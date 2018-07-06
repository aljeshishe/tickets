import pickle
import sys
from best import *
try:
   file_name = sys.argv[1]
except IndexError:
   file_name = 'best.pickle'

with open(file_name, 'rb') as f:
    data = pickle.load(f)
print(data)