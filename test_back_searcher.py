import pytest
from collections import defaultdict
from datetime import datetime, timedelta

from back_searcher import BackSearcher, Info


@pytest.fixture
def test_data():
    return [Info(depart_airport_code=1, depart_date_time=datetime(2018, 1, 1),
                 arrive_airport_code=2, arrive_date_time=datetime(2018, 1, 2),
                 duration=1, stop_count=0, price=1),
            Info(depart_airport_code=2, depart_date_time=datetime(2018, 1, 3),
                 arrive_airport_code=3, arrive_date_time=datetime(2018, 1, 4),
                 duration=1, stop_count=0, price=2),
            Info(depart_airport_code=1, depart_date_time=datetime(2018, 1, 4),
                 arrive_airport_code=2, arrive_date_time=datetime(2018, 1, 5),
                 duration=1, stop_count=0, price=3),
            Info(depart_airport_code=2, depart_date_time=datetime(2018, 1, 6),
                 arrive_airport_code=3, arrive_date_time=datetime(2018, 1, 7),
                 duration=1, stop_count=0, price=4),
            Info(depart_airport_code=1, depart_date_time=datetime(2018, 1, 7),
                 arrive_airport_code=2, arrive_date_time=datetime(2018, 1, 8),
                 duration=1, stop_count=0, price=5),
            Info(depart_airport_code=2, depart_date_time=datetime(2018, 1, 9),
                 arrive_airport_code=3, arrive_date_time=datetime(2018, 1, 10),
                 duration=1, stop_count=0, price=6)
            ]


def test(test_data):
    date = datetime(2018, 1, 11, 0, 0, 0)
    finish = 3
    start = 1

    searcher = BackSearcher(tickets=test_data, start=start, max_price=20, max_tickets=2)
    searcher.max_days_in_city = defaultdict(lambda: timedelta(2))
    searcher.max_days_in_city[finish] = timedelta(5)

    result = searcher.search(finish, date)
    assert result.tickets[0].price == 4
    assert result.tickets[0].tickets[0].price == 3
    assert result.tickets[1].price == 6
    assert result.tickets[1].tickets[0].price == 5


def test_max_price(test_data):
    date = datetime(2018, 1, 11, 0, 0, 0)
    finish = 3
    start = 1

    searcher = BackSearcher(tickets=test_data, start=start, max_price=10, max_tickets=2)
    searcher.max_days_in_city = defaultdict(lambda: timedelta(2))
    searcher.max_days_in_city[finish] = timedelta(5)

    result = searcher.search(finish, date)
    assert result.tickets[0].price == 4
    assert result.tickets[0].tickets[0].price == 3


def test_neighbours(test_data):
    date = datetime(2018, 1, 11, 0, 0, 0)
    finish = 3
    start = 1

    searcher = BackSearcher(tickets=test_data, start=start, max_price=10, max_tickets=2)
    searcher.max_days_in_city = defaultdict(lambda: timedelta(2))
    searcher.max_days_in_city[finish] = timedelta(5)
    searcher.add_neighbour(1, 2)

    result = searcher.search(finish, date)
    assert result.tickets[0].price == 4
    assert result.tickets[0].tickets[0].price == 0
    assert result.tickets[0].tickets[1].price == 3
    assert result.tickets[1].price == 6
    assert result.tickets[1].tickets[0].price == 0
    assert result.tickets[1].tickets[1].price == 5
