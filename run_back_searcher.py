
# result = Session.query(Ticket).order_by(Ticket.depart_date_time).all()
from collections import defaultdict

import time
from datetime import datetime, timedelta

import db
import model
from back_searcher import Ticket, BackSearcher, Path

tickets = db.Session.query(model.Ticket). \
    filter(model.Ticket.depart_date_time > '2018-08-01'). \
    filter(model.Ticket.arrive_date_time < '2018-09-30 00:00:00'). \
    filter(model.Ticket.price < 8000). \
    order_by(model.Ticket.depart_date_time).all()
print('Got %s records from db' % len(tickets))

date = datetime(2018, 9, 30, 0, 0, 0)
finish = 'LED'
start = 'BOJ'
searcher = BackSearcher(tickets=tickets, start=start, max_price=8000, max_tickets=2)
searcher.max_days_in_city = defaultdict(lambda: timedelta(1))
searcher.max_days_in_city[finish] = timedelta(60)
#searcher.add_neighbour('LED', 'VKO')
#searcher.add_neighbour('LED', 'DME')
#searcher.add_neighbour('LED', 'SVO')

start_time = time.time()
result = searcher.search(finish, date)
print('Results in %s secs' % (time.time() - start_time))
