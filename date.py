import datetime

class Date:

	# Get's the date today
    def todays_date(self):
        date_time = str(datetime.datetime.now())
        split_dt = date_time.split()
        today_date = split_dt[0]

        return today_date
