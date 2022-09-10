from datetime import datetime, timedelta

today = datetime.now()

date_before, date_after = "", ""
for i in range(1, 8):
    date_before = today - timedelta(days=7)
    date_after = today
    today = date_before
    print(today, date_after)
