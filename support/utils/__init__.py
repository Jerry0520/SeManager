import time
from datetime import datetime


def to_int_datetime(value):
    try:
        to_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        to_time = time.mktime(to_date.timetuple())
        return to_time * 1000
    except Exception as e:
        return 0


def to_str_datetime(value):
    if value is None or value == 0:
        return ''
    if type(value) == int:
        to_time = time.localtime(value / 1000)
        return time.strftime('%Y-%m-%d %H:%M:%S', to_time)
    if type(value) == datetime:
        return value.strftime('%Y-%m-%d %H:%M:%S')


def to_datetime(value):
    if value != '':
        to_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return to_date
    return None

if __name__ == '__main__':
    print(to_int_datetime('2017-7-25 16:50:50'))