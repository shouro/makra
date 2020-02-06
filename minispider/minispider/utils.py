from datetime import datetime, date, timedelta

bnn_enn = {'১':'1','২':'2','৩':'3','৪':'4','৫':'5','৬':'6','৭':'7','৮':'8','৯':'9','০':'0'}

def bangla_number_to_en(banglanum = '০'):
    return int(''.join((bnn_enn[n] for n in banglanum)))

def date_gen(start_date, end_date):
    return (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1))
