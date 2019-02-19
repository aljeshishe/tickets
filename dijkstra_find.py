from operator import itemgetter

import time

import itertools
import sys

import heapq
from collections import defaultdict

from datetime import timedelta

from model import Ticket
from db import Session


class N:
    def __init__(self, id):
        self.id = id
        self.prev = None
        self.price = None

    def __lt__(self, other):
        return False

    def __repr__(self):
        return 'N%s' % self.id


def Dijkstra(graph, source):
    queue = [(0, source, None)]
    while queue:
        path_len, start, prev = heapq.heappop(queue)
        if start.price is None:
            start.prev = prev
            start.price = path_len
            for end, edge_len in graph[start].items():
                if end.price is None:
                    heapq.heappush(queue, (path_len + edge_len, end, start))


def test():
    n1 = N(1)
    n2 = N(2)
    n3 = N(3)
    n4 = N(4)
    n5 = N(5)
    n6 = N(6)

    graph = {
      n1: {n2: 7, n3: 9, n6: 14},
      n2: {n4: 15, n3: 10, n1: 7},
      n3: {n1: 9, n2: 10, n4: 11, n6: 2},
      n4: {n3: 11, n5: 6},
      n5: {n4: 6, n6: 9},
      n6: {n1: 14, n3: 2, n5: 9}
    }
    source = n1

    Dijkstra(graph, source)
    for n in graph.keys():
        print(n)

test()

class Node:
    def __init__(self, code, date, ticket):
        self.prev = None
        self.price = None
        self.code = code
        self.date = date
        self.ticket = ticket

    def __lt__(self, other):
        return False

    def __str__(self):
        return '%s %s: %s %s' % (id(self), self.code, self.date.strftime('%m-%d %H-%M'), self.price)

    __repr__ = __str__


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def prepare(night_price=0):
    #result = Session.query(Ticket).order_by(Ticket.depart_date_time).all()
    result = Session.query(Ticket).\
        filter(Ticket.depart_date_time > '2018-10-10').\
        filter(Ticket.arrive_date_time < '2018-10-21 15:00:00').\
        filter(Ticket.price < 8000).\
        order_by(Ticket.depart_airport_code).\
        order_by(Ticket.depart_date_time).all()
    print('Got %s records from db' % len(result))
    graph = defaultdict(dict)
    cities = defaultdict(list)

    for ticket in result:
        # print(ticket)
        node1 = Node(ticket.depart_airport_code, ticket.depart_date_time, ticket)
        node2 = Node(ticket.arrive_airport_code, ticket.arrive_date_time, ticket)
        cities[ticket.depart_airport_code].append(node1)
        cities[ticket.arrive_airport_code].append(node2)
        graph[node2][node1] = ticket.price

    for k, nodes in cities.items():
        nodes.sort(key=lambda node: node.date)
        for pair in pairwise(nodes):
            if pair[1]:
                price = 0
                if night_price:
                    a = pair[1].date - timedelta(hours=3)
                    b = pair[0].date - timedelta(hours=3)
                    if (a.date() - b.date()).days:
                        print('Night %s %s' % (pair[0], pair[1]))
                        price = night_price
                graph[pair[1]][pair[0]] = price
    return graph, cities


def output(graph, cities):
    for src in ['RIX', 'LED', 'TLL', 'HEL', 'VKO', 'DME', 'SVO']:
        filtered = list(filter(lambda node: node.price, cities[src]))
        results = set()
        for i, nodes in enumerate(filtered):
            short_path = []
            prev = None
            cur = nodes
            while cur:
                if prev and cur.code != prev.code:
                    short_path.append(cur.ticket)
                prev = cur
                cur = cur.prev
            #print(short_path)
            results.add((nodes.price, sum([ticket.price for ticket in short_path]), tuple(short_path)))
            pass
        for total_price, tickets_price, tickets in sorted(results, key=itemgetter(0)):
            print(total_price, tickets_price, tickets)


graph, cities = prepare(night_price=0)
dest = cities['PMI'][-1]
print('Searching to %s' % dest)
start = time.time()

Dijkstra(graph, dest)
output(graph, cities)

print('Done %s' % (time.time() - start))
