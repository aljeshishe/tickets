import logging.config
import pathlib
from datetime import datetime


def configure():
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
                'filename': 'logs/tickets_%s.log' % datetime.now().strftime("%d%m%y_%H%M%S"),
                'formatter': 'verbose',
                'mode': 'w',
                'encoding': 'utf8',
            },
            'proxybroker_file_handler': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/proxybroker_%s.log' % datetime.now().strftime("%d%m%y_%H%M%S"),
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
    pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(log_config)
