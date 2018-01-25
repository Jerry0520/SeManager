from datetime import datetime

def to_datetime(value):
    if value != '':
        to_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return to_date
    return None