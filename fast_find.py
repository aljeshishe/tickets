from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import datetime, timedelta

import time

from heapq import heappush, heappop
from model import Ticket, Session


def bisect_left(a, x, key_name, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if getattr(a[mid], key_name) < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_right(a, x, key_name, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < getattr(a[mid], key_name):
            hi = mid
        else:
            lo = mid + 1
    return lo


class Node:
    def __init__(self, ticket):
        self.__dict__.update(ticket.__dict__)
        del self.__dict__['_sa_instance_state']

    def __str__(self):
        return 'Node[%s(%s)->%s(%s) %s %s %s]' % (self.depart_airport_code, self.depart_date_time.strftime('%m-%d %H-%M'),
                                                  self.arrive_airport_code, self.arrive_date_time.strftime('%m-%d %H-%M'),
                                                  self.duration, self.stop_count, self.price)

    __repr__ = __str__


#result = Session.query(Ticket).order_by(Ticket.depart_date_time).all()
result = Session.query(Ticket).filter(Ticket.depart_date_time > '2018-10-10').filter(Ticket.price < 5000).order_by(Ticket.depart_date_time).all()
print('Got %s records from db' % len(result))
data = defaultdict(lambda: defaultdict(list))
for ticket in result:
    data[ticket.depart_airport_code][ticket.arrive_airport_code].append(Node(ticket))

start = 'RIX'
finish = 'PMI'
max_tickets = 5
max_days_in_city = defaultdict(lambda: timedelta(2))
max_days_in_city[start] = timedelta(5)
results = []


class Path:
    def __init__(self):
        self.path = []
        self.cost = 0

    def copy(self):
        p = Path()
        p.path = list(self.path)
        p.cost = self.cost
        return p

    def __lt__(self, other):
        return self.cost > other.cost

    def __str__(self):
        return '%s %s' % (self.cost, self.path)

    __repr__ = __str__


def on_result(new_path):
    global results
    heappush(results, new_path)
    if len(results) > 10:
        heappop(results)


def bisect_range(tickets, start, end):
    i_start = bisect_right(tickets, start, key_name='depart_date_time')
    if i_start == len(tickets):
        return []

    i_end = bisect_left(tickets, end, key_name='depart_date_time')
    if not i_end:
        return []
    return tickets[i_start:i_end]


def search(city, path, date):
    visited = [ticket.depart_airport_code for ticket in path.path]
    visited.append(city)
    for dest, tickets in data[city].items():
        if dest in visited:
            continue
        fileterd_tickets = bisect_range(tickets, date, date + max_days_in_city[city])
        if not fileterd_tickets:
            return

        if len(visited) == 1:
            print(visited, dest)
            for result in results:
                print(result)

        for ticket in fileterd_tickets:
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
