import itertools
import logging
import logging.config
from datetime import date
from functools import partial

import db
import model
import proxied_requests
from model import task, SQLALCHEMY_DATABASE_NAME
from processor import Processor
from results import *
from utils import date_range

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
            'format': '%(asctime)s.%(msecs)03d|%(levelname)-4.4s|%(thread)-6.6s|%(funcName)-10.10s|%(message)s',
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
        'console_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'requests': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['file_handler', 'console_handler'],
        'level': 'DEBUG',
        'propagate': False,
    }
}


if __name__ == '__main__':
    logging.config.dictConfig(log_config)
    airports = ['BERL', 'BOJ', 'BRE', 'BTS', 'BUD', 'CGN', 'DEB', 'DUS', 'HAJ', 'HAM', 'LED', 'LTN', 'MILA', 'MOSC', 'MUC', 'PARI', 'PMI', 'STR', 'TLL', 'RIX', 'VNO', 'VIE', 'CIA']
    tasks = generator(task=task,
                      depart=airports,
                      arrive=airports,
                      date=date_range(date(2018, 10, 16),6),
                      requests=proxied_requests.Requests())
    p = Processor(10)
    p.run(tasks)
