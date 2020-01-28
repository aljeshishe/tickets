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

# STOC сктокгольм
# MOSC москва
# #победа лиетает из питера
# TXL Берлин
# GRO Жирона
# CGN Кельн
# BGY Бергамо
# SAW Стамбул
# TBS тбилиси
# KGD калининград
# from led
# to = ('BUD','TXL','GRO','CGN','BGY','SAW','TBS','KGD','MLA', 'PSA', 'STN')
# from VKO pobeda wizz air non RU
# to = ['AYT', 'BGY', 'BTS', 'BUD', 'CGN', 'DEB', 'FKB', 'FMM', 'GRO', 'HEL', 'IST', 'KLV', 'LCA', 'LEJ', 'LWN', 'PMO', 'PSA', 'SAW', 'SZG', 'TIV', 'TSF', 'TXL']
if __name__ == '__main__':
    p = Processor(30)
    requests = proxied_requests.Requests()
    today = date.today()
    # to = 'LPP ATH SKG BGY' # from lpp
    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 90),
    #                       depart=to.split(),
    #                       arrive=to.split(),
    #                       requests=requests,
    #                       max_price=6000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 7, 1), 90),
    #                       depart='KFU KLX SKG ATH HEL LPP HER RHO'.split(),
    #                       arrive='KFU KLX SKG ATH HEL LPP HER RHO'.split(),
    #                       requests=requests,
    #                       max_price=10000))

    # from led all
    # to = ["ALC", "ALA", "AMS", "AAQ", "AYT", "KVK", "ARH", "ASB", "ATH", "GYD", "BCN", "BAX", "NBC", "PEK", "EGO", "BEG", "BGY", "SXF", "TXL", "OGZ", "FRU", "BOJ", "BRU", "BZK", "BUD", "BHK", "CSY", "CEK", "CTU", "CEE", "MRV", "CIT", "KIV", "CGN", "CPH", "DJE", "DOH", "DRS", "DXB", "DYU", "DUS", "VDA", "NBE", "FEG", "FRA", "KVD", "GVA", "GRV", "HAM", "HEL", "INN", "IKT", "SAW", "IST", "IWA", "IJK", "ADB", "KGD", "KLF", "KZN", "LBD", "KVX", "KRR", "KJA", "URS", "LCA", "LPK", "LGW", "STN", "LHR", "MAD", "MCX", "MXP", "MSQ", "MIR", "DME", "VKO", "SVO", "MUC", "MMK", "NYM", "NAL", "NMA", "NNM", "NVI", "NCE", "GOJ", "NSK", "OVB", "NUX", "NOJ", "OLB", "OMS", "REN", "OSS", "CDG", "PEE", "PSA", "PRG", "PUY", "RIX", "RMI", "FCO", "ROV", "SLY", "SZG", "KUF", "SKD", "SYX", "SKX", "ICN", "SIP", "AER", "STW", "ARN", "SGC", "SVX", "SCW", "TLL", "TBW", "TAS", "TBS", "IKA", "TLV", "TMJ", "SKG", "TIV", "TSE", "TUN", "TJM", "UFA", "UCT", "ULV", "UGC", "URC", "USK", "MLA", "VRA", "VRN", "VIE", "VOG", "VOZ", "WAW", "YKS", "IAR", "EVN", "ZAG", "ZRH"]
    # to = ['AYT', 'BGY', 'BTS', 'BUD', 'CGN', 'DEB', 'FKB', 'FMM', 'GRO', 'HEL', 'IST', 'KLV', 'LCA', 'LEJ', 'LWN', 'PMO', 'PSA', 'SAW', 'SZG', 'TIV', 'TSF', 'TXL']
    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 90),
    #                       depart='LED'.split(),
    #                       arrive=to,
    #                       requests=requests,
    #                       max_price=10000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date.today(), 90),
    #                       depart=to,
    #                       arrive='LED'.split(),
    #                       requests=requests,
    #                       max_price=10000))

    # from tll
    # to = ['BGY', 'DUB', 'EDI', 'GRO', 'IEV', 'LGW', 'MLA', 'MXP', 'NRN', 'PFO', 'STN', 'SXF']
    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 90),
    #                       depart='TLL'.split(),
    #                       arrive=to,
    #                       requests=requests,
    #                       max_price=6000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 90),
    #                       depart=to,
    #                       arrive='TLL'.split(),
    #                       requests=requests,
    #                       max_price=6000))


    # to = ['BFS', 'BRS', 'BSL', 'BUD', 'EDI', 'GDN', 'GVA', 'KTW', 'LGW', 'LTN', 'MAN', 'RIX', 'STN', 'VIE', 'VNO', 'WAW', 'WRO']
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 6, 14), 20),
    #                       depart='KEF'.split(),
    #                       arrive=to,
    #                       requests=requests,
    #                       max_price=8000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 6, 14), 20),
    #                       depart=to,
    #                       arrive='KEF'.split(),
    #                       requests=requests,
    #                       max_price=8000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 28), 30),
    #                       depart='HEL STOC COPE'.split(),
    #                       arrive='HEL STOC COPE'.split(),
    #                       requests=requests,
    #                       max_price=6000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 90),
    #                       depart='LED BUD'.split(),
    #                       arrive='LED BUD'.split(),
    #                       requests=requests,
    #                       max_price=8000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(today, 120),
    #                       depart='LED KGD'.split(),
    #                       arrive='LED KGD'.split(),
    #                       requests=requests,
    #                       max_price=8000))
    # to = ['ACE', 'AMS', 'ARN', 'BCN', 'BFS', 'BHX', 'BRE', 'BRS', 'BRU', 'BSL', 'CGN', 'CPH', 'DRS', 'DUS', 'EDI', 'EMA', 'ERF', 'FMO', 'FRA', 'FUE', 'GLA', 'GVA', 'HAJ', 'HAM', 'HEL', 'LBA', 'LEJ', 'LGW', 'LIS', 'LPA', 'LUX', 'MAD', 'MAN', 'MUC', 'NCL', 'NUE', 'OPO', 'ORY', 'OSL', 'PDL', 'PRG', 'PXO', 'SCQ',\
    #      'STN', 'STR', 'TFN', 'TFS', 'TLS', 'TXL', 'VIE', 'ZRH']
    to = ['HEL']
    p.add_tasks(generator(task=task,
                          date=date_range(date(2020, 1, 9), 5),
                          depart='FNC'.split(),
                          arrive=to,
                          requests=requests,
                          max_price=8000))

    # to = ['LPK', 'KLV', 'VOZ', 'TBW', 'BZK', 'URS', 'GOJ', 'SKX', 'KZN', 'ULW', 'IWA', 'MOSC', 'PEZ']
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 5, 5), 10),
    #                       depart='LED'.split(),
    #                       arrive=to,
    #                       requests=requests,
    #                       max_price=6000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 5, 5), 10),
    #                       depart=to,
    #                       arrive='LED'.split(),
    #                       requests=requests,
    #                       max_price=6000))
    #
    p.wait_done()
    p.stop()
