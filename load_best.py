import pickle
import sys
from best import *
try:
   file_name = sys.argv[1]
except IndexError:
   file_name = 'best.pickle'

with open(file_name, 'rb') as f:
    data = pickle.load(f)
cities = ['LED', 'PMI', 'RIX', 'TLL', 'HEL', 'VKO', 'DME', 'SVO']
for city in cities:
    print(city)
    print('destinations')
    for item in filter(lambda pair: pair[1] < 3000, data[city].destinations):
        print(item)

    print('sources')
    for item in filter(lambda pair: pair[1] < 3000, data[city].sources):
        print(item)
print(data)
