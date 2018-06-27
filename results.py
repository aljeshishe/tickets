from datetime import datetime
import operator
from utils import as_list, shorten, as_string

__author__ = 'alexey.grachev'

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class Result:
    def __init__(self, **kwargs):
        self.args = AttrDict(kwargs)

    def __str__(self):
        args = self.args
        log = '{city:<10};\t{dateFrom};\t{day};\t{country:<10};\t{days};\t{count};\t{prices}\t{request}\n' \
            .format(city=args.city,
                    dateFrom=asRevString(args.date),
                    day=args.date.weekday()+1,
                    days=args.days,
                    country=args.country,
                    count=args.count,
                    prices=args.prices,
                    request=args.request)
        return log

    def __lt__(self, other):
        return str(self) < str(other)

def fileName(cities, contries, dates, days):
    return '{cities}-{countries}_{date}-{days}_{postfix}.csv'.\
        format(cities='+'.join(shorten(as_list(cities))),
               countries='+'.join(shorten(as_list(contries))),
               date=as_string(dates[0]),
               days=days,
               postfix=datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S"))

class Logger:
    def __init__(self, iter, filename):
        items = sorted(map(str, iter))
        for item in items:
            print(item, end='')
        with open(filename, 'a', encoding='utf-8') as file:
            file.writelines(items)
