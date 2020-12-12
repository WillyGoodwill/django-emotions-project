import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
import django
django.setup()

# Fake pop script

from basic_app.models import Stocks2

import pandas as pd
import yfinance as yf
import datetime


def add_topic(date,AAPL,TSLA):
    print(date)
    t = Stocks2.objects.get_or_create(date = date,
    AAPL = AAPL,
    TSLA = TSLA)[0]
    print(t.date)
    t.save()
    return t

tickers_list = ['AAPL','TSLA']

data = pd.DataFrame(columns=tickers_list)

for ticker in tickers_list:
    data[ticker] = yf.download(ticker,'2016-12-10','2020-12-11')['Adj Close']

data = data.reset_index()
# format date 
data['Date2'] = pd.to_datetime(data['Date']).apply(lambda x: x.strftime('%Y-%m-%d'))

for i in range(len(data['AAPL'])):
    date = data['Date2'][i]
    AAPL = data['AAPL'][i]
    TSLA = data['TSLA'][i]
    add_topic(date,AAPL,TSLA)


    
# if __name__ == '__main__':
#     populate(20)
#     print('populating complete')