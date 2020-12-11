import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
import django
django.setup()

# Fake pop script

from basic_app.models import Stocks

import pandas as pd
import yfinance as yf
import datetime


def add_topic():
    t = Stocks.objects.get_or_create(date = date,
    AAPL = AAPL,
    TSLA = TSLA)[0]
    t.save()
    return t

tickers_list = ['AAPL','TSLA']

data = pd.DataFrame(columns=tickers_list)

for ticker in tickers_list:
    data[ticker] = yf.download(ticker,'2016-12-01','2020-12-09')['Adj Close']

data = data.reset_index()

for i in range(len(data['AAPL'])):
    date = data.iloc[:i+1,0][0]
    AAPL = data['AAPL'][i]
    TSLA = data['TSLA'][i]

    add_topic()


    
# if __name__ == '__main__':
#     populate(20)
#     print('populating complete')