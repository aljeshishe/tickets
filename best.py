import datetime
import logging
import pickle
from collections import defaultdict
from functools import partial
from operator import attrgetter
from threading import RLock

import sys

import proxied_requests
from processor import Processor
from utils import date_range


class Node:
    def __init__(self, code):
        self.code = code
        self.name = ''
        self.dst = {}
        self.src = {}

    def to(self, dest, price):
        self.dst[dest] = price
        dest.src[self] = price

    @property
    def sources(self):
        return list(sorted(self.src.items(), key=lambda i: i[1]))

    @property
    def destinations(self):
        return list(sorted(self.dst.items(), key=lambda i: i[1]))

    @property
    def priority(self):
        return len(self.src) + len(self.dst)

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return '{} {} sources:{} min:{} destinations:{} min:{}'.format(self.code, self.name, len(self.src), min(self.src.values() or [0]),
                                                                       len(self.dst), min(self.dst.values() or [0]))
    __repr__ = __str__


requests = proxied_requests.Requests()
results = {}
processed = set()
proc = Processor(60)
lock = RLock()


def best(start, depth):
    with lock:
        if start in processed:
            return
        print('Processing {} {}(processed {}/{} results:{})'.format(depth, start, len(processed), len(proc), len(results)))
        processed.add(start)
    depth -= 1
    top_price = 5000
    resp = requests.get('https://lyssa.aviasales.ru/map?origin_iata={}&one_way=true&min_trip_duration=1&max_trip_duration=30'.format(start))
    resp.raise_for_status()
    data = resp.json()
    for item in data:
        price = item['value']
        if price < top_price:
            src = item['origin']
            dst = item['destination']
            with lock:
                start_node = results.setdefault(src, Node(start))
                dest_node = results.setdefault(dst, Node(dst))
                dest_node.name = ''
                start_node.to(dest_node, price)
                if dst in processed or depth < 0:
                    continue
            proc.add(partial(best, start=dst, depth=depth))


if __name__ == '__main__':
    starts = ['LED', 'PMI']
    for start in starts:
        proc.add(partial(best, start=start, depth=5))
    proc.wait_done()
    for result in sorted(results.values(), key=attrgetter('priority')):
        print('{}'.format(result))

    with open('best.pickle', 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    proc.stop()
