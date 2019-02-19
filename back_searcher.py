from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import timedelta
from itertools import chain
from operator import attrgetter

import sys


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


class Info:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class Ticket:
    def __init__(self, ticket=None):
        if ticket:
            self.__dict__.update(ticket.__dict__)
            self.__dict__.pop('_sa_instance_state', None)
        self.sum = None
        self.count = 0
        self.tickets = []

    def __str__(self):
        return 'Ticket[%s(%s)->%s(%s) d:%s s:%s %s/%s]' % (self.depart_airport_code, self.depart_date_time.strftime('%m-%d %H-%M'),
                                                           self.arrive_airport_code, self.arrive_date_time.strftime('%m-%d %H-%M'),
                                                           self.duration, self.stop_count, self.price, self.sum)

    __repr__ = __str__


class StartTicket:
    def __init__(self, city, depart_date_time):
        self.depart_airport_code = city
        self.depart_date_time = depart_date_time
        self.price = 0
        self.sum = 0
        self.count = 0
        self.tickets = []

    def __str__(self):
        return 'StartTicket[%s(%s) %s/%s]' % (self.depart_airport_code, self.depart_date_time.strftime('%m-%d %H-%M'),
                                              self.price, self.sum)

    __repr__ = __str__


class Path(set):
    def __init__(self):
        super().__init__()
        self.price = 0

    def add(self, city, price):
        super(Path, self).add(city)
        self.price += price

    def remove(self, city, price):
        super(Path, self).remove(city)
        self.price -= price


def bisect_range(tickets, start, end, key_name):
    i_start = bisect_right(tickets, start, key_name=key_name)
    if i_start == len(tickets):
        return []

    i_end = bisect_left(tickets, end, key_name=key_name)
    if not i_end:
        return []
    return tickets[i_start:i_end]


class BackSearcher:
    def __init__(self, tickets, start, max_price, max_tickets):
        self.data = defaultdict(lambda: defaultdict(list))
        for ticket in tickets:
            self.data[ticket.arrive_airport_code][ticket.depart_airport_code].append(Ticket(ticket))
        self.finish = start
        self.max_price = max_price
        self.max_tickets = max_tickets
        self.max_days_in_city = None
        self.neighbours = defaultdict(list)

    def add_neighbour(self, start, finish):
        self.neighbours[start].append(finish)
        self.neighbours[finish].append(start)

    def search(self, finish, date):
        result = StartTicket(finish, date)
        path = Path()
        self._search(path, result)
        return result

    def _neighbour_tickets(self, city, date):
        for depart_city in self.neighbours.get(city, []):
            ticket = Ticket(Info(depart_airport_code=depart_city, depart_date_time=date - timedelta(minutes=1),
                                 arrive_airport_code=city, arrive_date_time=date - timedelta(minutes=2),
                                 duration=0, stop_count=0, price=0))
            yield depart_city, [ticket]

    def _search(self, path, prev_ticket=None):
        city = prev_ticket.depart_airport_code
        date = prev_ticket.depart_date_time
        path.add(city, prev_ticket.price)
        min = sys.maxsize
        for depart_city, tickets in chain(self._neighbour_tickets(city, date), self.data[city].items()):
            if depart_city in path:
                continue
            filtered_tickets = bisect_range(tickets, date - self.max_days_in_city[city], date, key_name='arrive_date_time')
            if not filtered_tickets:
                continue

            for ticket in filtered_tickets:
                if ticket.depart_airport_code == self.finish:
                    ticket.sum = ticket.price
                else:
                    sum = sys.maxsize
                    if len(path) + 1 <= self.max_tickets and path.price + ticket.price < self.max_price:
                        sum = self._search(path, ticket)
                    if sum is sys.maxsize:
                        continue
                    ticket.sum = ticket.price + sum
                if ticket.sum > self.max_price:
                    continue
                prev_ticket.tickets.append(ticket)
                if ticket.sum < min:
                    min = ticket.sum
        path.remove(city, prev_ticket.price)
        prev_ticket.tickets.sort(key=attrgetter('sum'))
        return min
