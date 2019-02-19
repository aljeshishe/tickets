from collections import defaultdict, deque
from copy import copy
import time
from datetime import datetime

from heapq import heappush, heappop
from model import Ticket
from db import Session


class Path:
    def __init__(self):
        self.path = []
        self.cost = 0

    def copy(self):
        p = Path()
        p.path = copy(self.path)
        p.cost = self.cost
        return p

    def __lt__(self, other):
        return self.cost > other.cost

    def __str__(self):
        return '%s %s' % (self.cost, self.path)

    __repr__ = __str__


def bisect_right(a, x, arg_name):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    lo=0
    hi=None
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x < getattr(a[mid], arg_name): hi = mid
        else: lo = mid+1
    return lo


result = Session.query(Ticket).filter(Ticket.depart_date_time > '2018-10-10').filter(Ticket.price < 5000).order_by(Ticket.depart_date_time).all()
print('Got %s records from db' % len(result))
data = defaultdict(list)
for ticket in result:
    data[ticket.depart_airport_code].append(ticket)

start = 'HAM'
finish = 'TXL'
max_tickets = 5

results = []


def on_result(new_path):
    global results
    heappush(results, new_path)
    if len(results) > 10:
        heappop(results)


def search(city, path, date):
    tickets = data[city]
    i = bisect_right(tickets, date, 'depart_date_time')
    if i == len(tickets):
        return
    visited = [ticket.depart_airport_code for ticket in path.path]
    visited.append(city)
    if len(visited) < 3:
        print(visited)
        for result in results:
            print(result)
    for ticket in tickets[i:]:
        if ticket.arrive_airport_code in visited:
            continue
        new_path = path.copy()
        new_path.path.append(ticket)
        new_path.cost += ticket.price
        if ticket.arrive_airport_code == finish:
            on_result(new_path)
            continue
        if len(new_path.path) == max_tickets:
            continue
        search(ticket.arrive_airport_code, new_path, ticket.arrive_date_time)


start_time = time.time()
p = Path()
date = datetime(2018, 10, 15)
search(start, p, date)
print('Results in %s secs' % (time.time() - start_time))
for result in sorted(results, key=lambda result: result.cost):
    print(result)
