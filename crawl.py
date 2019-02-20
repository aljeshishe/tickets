import logging
import log_config
from datetime import date

import proxied_requests
from generator import generator
from model import task
from processor import Processor
from utils import date_range

log = logging.getLogger(__name__)
log_config.configure()
__author__ = 'alexey.grachev'

# MOSC москва
# #победа лиетает из питера
# TXL Берлин
# GRO Жирона
# CGN Кельн
# BGY Бергамо
# SAW Стамбул
# TBS тбилиси
# KGD калининград
# BRQ PED DRS SXF
if __name__ == '__main__':
    p = Processor(60)
    requests = proxied_requests.Requests()
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='LED CMB'.split(),
    #                       arrive='LED CMB'.split(),
    #                       requests=requests,
    #                       max_price=40000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='MOSC CMB '.split(),
    #                       arrive='MOSC CMB'.split(),
    #                       requests=requests,
    #                       max_price=40000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='LED PEZ'.split(),
    #                       arrive='LED PEZ'.split(),
    #                       requests=requests,
    #                       max_price=10000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='MOSC PEZ'.split(),
    #                       arrive='MOSC PEZ'.split(),
    #                       requests=requests,
    #                       max_price=10000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='LED ARN'.split(),
    #                       arrive='LED ARN'.split(),
    #                       requests=requests,
    #                       max_price=10000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 22), 30),
    #                       depart='MOSC ARN'.split(),
    #                       arrive='MOSC ARN'.split(),
    #                       requests=requests,
    #                       max_price=10000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 3, 1), 60),
    #                       depart='MOSC LCA'.split(),
    #                       arrive='MOSC LCA'.split(),
    #                       requests=requests,
    #                       max_price=10000))

    p.add_tasks(generator(task=task,
                          date=date_range(date(2019, 3, 1), 90),
                          depart='BUD LED'.split(),
                          arrive='BUD LED'.split(),
                          requests=requests,
                          max_price=10000))
    p.wait_done()
    p.stop()
