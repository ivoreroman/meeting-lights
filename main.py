import random
from datetime import datetime, timedelta

from repeated_timer import RepeatedTimer


def gen_datetime(min_year=2018, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    date = start + (end - start) * random.random()
    print(date)


if __name__ == '__main__':
    timer = RepeatedTimer(2, gen_datetime)
    timer.start()
