import itertools
import logging.config
from datetime import date, datetime
from functools import partial
import proxied_requests
from model import task, SQLALCHEMY_DATABASE_NAME
from processor import Processor
from utils import date_range, as_list

log = logging.getLogger(__name__)
__author__ = 'alexey.grachev'


def generator(task, **kwargs):
    keys = []
    values = []
    for k, v in kwargs.items():
        keys.append(k)
        values.append(as_list(v))
    args_list = [dict(zip(keys, items)) for items in itertools.product(*values)]
    for args in args_list:
        yield partial(task, **args)


log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s.%(msecs)03d|%(levelname)-4.4s|%(thread)-6.6s|%(module)-6.6s|%(funcName)-10.10s|%(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    },
    'handlers': {
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'tickets_%s.log' % datetime.now().strftime("%d%m%y_%H%M%S"),
            'formatter': 'verbose',
            'mode': 'w',
            'encoding': 'utf8',
        },
        'proxybroker_file_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'proxybroker_%s.log' % datetime.now().strftime("%d%m%y_%H%M%S"),
            'formatter': 'verbose',
            'mode': 'w',
            'encoding': 'utf8',
        },
        'console_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'proxybroker': {
            'handlers': ['proxybroker_file_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'proxied_requests': {
            'handlers': ['proxybroker_file_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'urllib3': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['file_handler', 'console_handler'],
        'level': 'DEBUG',
        'propagate': False,
    }
}

airports ='''AGP
ALC
AMS
ARN
ATH
BCN
BGO
BGY
BIO
BOJ
BRE
BRI
BUD
BVA
CGN
CIA
CPH
CRL
DME
DUB
DUS
FCO
FMO
FRA
GDN
GVA
HAJ
HEL
IEV
LED
LEJ
LGW
LIS
LTN
MAD
MLA
MUC
MXP
OSL
OTP
PMI
PRG
PSA
RIX
SAW
SOF
STN
STR
SVO
SVQ
SXF
TLL
TXL
VAR
VIE
VKO
VLC
VNO
WAW'''
if __name__ == '__main__':
    logging.config.dictConfig(log_config)
    # 23! * 5 2635
    # 22 2410
    # 21 2195
    # airports = ['BERL', 'BOJ', 'BRE', 'BTS', 'BUD', 'CGN', 'DEB', 'DUS', 'HAJ', 'HAM', 'LED', 'LTN', 'MILA', 'MOSC', 'MUC', 'PARI', 'PMI', 'STR', 'TLL', 'RIX', 'VNO', 'VIE', 'CIA']
    airports = airports.split()
    print('Airports: %s' % len(airports))
    p = Processor(30)
    requests = proxied_requests.Requests()
    tasks = generator(task=task,
                      date=date_range(date(2018, 10, 16), 5),
                      depart=airports,
                      arrive=airports,
                      requests=requests)
    p.add_tasks(tasks)
    tasks = generator(task=task,
                      date=date_range(date(2018, 11, 2), 5),
                      depart=airports,
                      arrive=airports,
                      requests=requests)
    p.add_tasks(tasks)
    p.wait_done()
    p.stop()
