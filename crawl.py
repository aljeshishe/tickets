import logging
from datetime import date

import proxied_requests
from generator import generator
from model import task
from processor import Processor
from utils import date_range

log = logging.getLogger(__name__)
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
    p.add_tasks(generator(task=task,
                          date=date_range(date(2019, 3, 28), 10),
                          depart='LED BRQ '.split(),
                          arrive='LED BRQ'.split(),
                          requests=requests,
                          max_price=10000))

    p.wait_done()
    p.stop()
