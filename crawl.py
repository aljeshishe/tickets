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
# from led
# to = ('BUD','TXL','GRO','CGN','BGY','SAW','TBS','KGD','MLA', 'PSA', 'STN')
# from led all
# to = ["ALC", "ALA", "AMS", "AAQ", "AYT", "KVK", "ARH", "ASB", "ATH", "GYD", "BCN", "BAX", "NBC", "PEK", "EGO", "BEG", "BGY", "SXF", "TXL", "OGZ", "FRU", "BOJ", "BRU", "BZK", "BUD", "BHK", "CSY", "CEK", "CTU", "CEE", "MRV", "CIT", "KIV", "CGN", "CPH", "DJE", "DOH", "DRS", "DXB", "DYU", "DUS", "VDA", "NBE", "FEG", "FRA", "KVD", "GVA", "GRV", "HAM", "HEL", "INN", "IKT", "SAW", "IST", "IWA", "IJK", "ADB", "KGD", "KLF", "KZN", "LBD", "KVX", "KRR", "KJA", "URS", "LCA", "LPK", "LGW", "STN", "LHR", "MAD", "MCX", "MXP", "MSQ", "MIR", "DME", "VKO", "SVO", "MUC", "MMK", "NYM", "NAL", "NMA", "NNM", "NVI", "NCE", "GOJ", "NSK", "OVB", "NUX", "NOJ", "OLB", "OMS", "REN", "OSS", "CDG", "PEE", "PSA", "PRG", "PUY", "RIX", "RMI", "FCO", "ROV", "SLY", "SZG", "KUF", "SKD", "SYX", "SKX", "ICN", "SIP", "AER", "STW", "ARN", "SGC", "SVX", "SCW", "TLL", "TBW", "TAS", "TBS", "IKA", "TLV", "TMJ", "SKG", "TIV", "TSE", "TUN", "TJM", "UFA", "UCT", "ULV", "UGC", "URC", "USK", "MLA", "VRA", "VRN", "VIE", "VOG", "VOZ", "WAW", "YKS", "IAR", "EVN", "ZAG", "ZRH"]
# from VKO pobeda wizz air non RU
# to = ['AYT', 'BGY', 'BTS', 'BUD', 'CGN', 'DEB', 'FKB', 'FMM', 'GRO', 'HEL', 'IST', 'KLV', 'LCA', 'LEJ', 'LWN', 'PMO', 'PSA', 'SAW', 'SZG', 'TIV', 'TSF', 'TXL']
# from lpp
# ('sxf','bgy','ath','skg')
if __name__ == '__main__':
    p = Processor(60)
    requests = proxied_requests.Requests()

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 20), 30),
    #                       depart='MOSC CMB'.split(),
    #                       arrive='MOSC CMB'.split(),
    #                       requests=requests,
    #                       max_price=40000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 3, 10), 90),
    #                       depart='LED'.split(),
    #                       arrive=to,
    #                       requests=requests,
    #                       max_price=10000))
    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 3, 10), 90),
    #                       depart=to,
    #                       arrive='LED'.split(),
    #                       requests=requests,
    #                       max_price=10000))
    to = ['AYT', 'BGY', 'BTS', 'BUD', 'CGN', 'DEB', 'FKB', 'FMM', 'GRO', 'HEL', 'IST', 'KLV', 'LCA', 'LEJ', 'LWN', 'PMO', 'PSA', 'SAW', 'SZG', 'TIV', 'TSF', 'TXL']
    p.add_tasks(generator(task=task,
                          date=date_range(date(2019, 3, 15), 120),
                          depart='VKO'.split(),
                          arrive=to,
                          requests=requests,
                          max_price=5000))

    # p.add_tasks(generator(task=task,
    #                       date=date_range(date(2019, 4, 23), 30),
    #                       depart='LED MOSC PEZ'.split(),
    #                       arrive='LED MOSC PEZ'.split(),
    #                       requests=requests,
    #                       max_price=10000))

    p.wait_done()
    p.stop()
