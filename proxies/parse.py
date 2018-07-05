import sys
import json
import re
from collections import defaultdict

d = defaultdict(lambda: defaultdict(int))
with open(sys.argv[1]) as f:
    for line in f:
        protos, domen = re.match('.+\[(.+)\].+ (.+)>', line).groups()
        protos = protos.split(', ')
        print(protos, domen)
        for proto in protos:
            proto = proto.replace(': ', '-')
            d[domen][proto] += 1
for domen, protos in d.items():
    print(domen, ' '.join(['%s:%s' % (k, v) for k, v in protos.items()]))
