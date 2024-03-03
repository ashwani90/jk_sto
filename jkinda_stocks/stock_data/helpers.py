from datetime import date, timedelta

def get_date_range_from_range(range):
    today = date.today()
    prev_date = today
    range = int(range)
    if range == int(1):
        prev_date =  today - timedelta(days=7)
    if range == int(4):
        prev_date =  today - timedelta(days=30)
    if range == int(500):
        prev_date =  today - timedelta(days=(365*5))
    if range == int(50):
        prev_date =  today - timedelta(days=365)
    return [prev_date,today]