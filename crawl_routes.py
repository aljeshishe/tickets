import argparse
import json
import logging
from contextlib import suppress
from functools import partial
from os import mkdir
from threading import RLock

import log_config

import requests

import proxied_requests
from airports import Route
from db import Session
from processor import Processor

log_config.configure()
log = logging.getLogger(__name__)

# parser = argparse.ArgumentParser(description='Process commands, for Elastic searching')
# parser.add_argument('airport', nargs=1, default='', help='input json with routes')
# args = parser.parse_args()

requests = proxied_requests.Requests()
results = {}
processed = set()
proc = Processor(120)
lock = RLock()


def crawl(airport, depth):
    with lock:
        if airport in processed:
            return
        print('Processing {} {}(processed {}/{})'.format(depth, airport, len(processed), len(proc)))
        processed.add(airport)

    resp = requests.get('https://www.flightsfrom.com/%s' % airport)
    resp.raise_for_status()
    data = resp.text
    _, _, data = data.partition('window.routes = ')
    data, _, _ = data.partition(';')
    data = json.loads(data)
    with open('routes/routes_%s.json' % airport, 'w') as f:
        f.write(json.dumps(data, indent=2))

    session = Session()
    try:
        for item in data:
            from_ = item['iata_from']
            to_ = item['iata_to']
            for route in item['airlineroutes']:
                carrier = route['carrier']
                carrier_name = route['carrier_name']
                if not from_ or not to_ or not carrier:
                    log.warning('Ignoring:\n%s' % json.dumps(item, indent=2))
                    continue
                route = Route()
                route.depart = from_
                route.arrive = to_
                route.carrier = carrier
                route.carrier_name = carrier_name
                session.merge(route)
                session.commit()
            if to_ in processed or depth < 0:
                continue
            proc.add(partial(crawl, airport=to_, depth=depth))
    except Exception:
        log.exception('Exception')
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    with suppress(FileExistsError):
        mkdir('routes')
    proc.add(partial(crawl, airport='LED', depth=2))
    proc.wait_done()
