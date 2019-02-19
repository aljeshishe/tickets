import argparse
import json
import sys

import requests

parser = argparse.ArgumentParser(description='Process commands, for Elastic searching')
parser.add_argument('airport', nargs=1, default='', help='input json with routes')
args = parser.parse_args()

resp = requests.get('https://www.flightsfrom.com/%s' % args.airport[0])
resp.raise_for_status()
data = resp.text
_, _, data = data.partition('window.routes = ')
data, _, _ = data.partition(';')


data = json.loads(data)
result_non_ru = []
result = []

for value in data:
    result.append(value['iata_to'])
    if value['airport']['country_code'] != 'RU':
        result_non_ru.append(value['iata_to'])

print('all: %s' % json.dumps(result))
print('non ru: %s' % json.dumps(result_non_ru))