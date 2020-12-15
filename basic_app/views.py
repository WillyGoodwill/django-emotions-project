from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls.base import reverse
from django.contrib import messages

from basic_app.models import (Emotions,EmotionsAvgTemperature, Stocks2, Stock,
 AboutMyView,AboutMyViewOthers,AboutMyViewFuture)
from basic_app.forms import (FormEmotions,FormEmotionsAvgTemperature,FormStocks2, StockForm,
 TestForm,TestForm2,TestForm3)

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import (TemplateView, ListView, DetailView, CreateView
# )
import requests
import random
from django.core.serializers.json import DjangoJSONEncoder
import json

import os
import pandas as pd
import datetime
import numpy as np

from django.db.models import Count
from django.db.models import Avg

def index(request):
    with open(os.path.join(os.path.dirname(os.getcwd()),'emotions_project/templates/basic_app/emotions_degree.json'), 'r') as json_file:

        data1 = json.load(json_file)
        data2 = data1[0]['Страх'] + data1[0]['Тоска'] + data1[0]['Гнев']+ data1[0]['Стыд']+ data1[0]['Радость']
        data3 = tuple([(k, v) for k,v in enumerate(data2)])

    value = random.choice(data3)
    className_lib = ['myYellowText','myRedText','myBlueText']
    if value[0]<50:
        className = className_lib[0]
    elif value[0]>=50 and value[0]<110:
        className = className_lib[1]
    else:
        className = className_lib[2]


    if request.method == 'POST':
        value = random.choice(data3)
        className_lib = ['myYellowText','myRedText','myBlueText']
        if value[0]<50:
            className = className_lib[0]
        elif value[0]>=50 and value[0]<110:
            className = className_lib[1]
        else:
            className = className_lib[2]
    return render(request,'basic_app/index.html',{'value':value[1],'className':className})

def emotions_form(request):
    form = FormEmotions()
    if request.method == 'POST':
        form = FormEmotions(request.POST)
        if form.is_valid():
            form.save(commit = True)
            form = FormEmotions()

        else:
            print('Form invalid')
       
        # process and save data to database: number of joy per day vs avg temp per day        
        # calc summary for the last date and save to DB, 
        # in DB will be several entries for this date, the last - the most actual
        date = Emotions.objects.values('date').filter(emotions ='5').annotate(total =Count('date')).order_by('-date').values('date')[0]
        joyfullness = list(Emotions.objects.values('date').filter(emotions ='5').annotate(total =Count('date')).order_by('-date').values('total')[0].values())[0]
        average_temperature = list(Emotions.objects.values('date').filter(emotions = '5').annotate(avg_temp = Avg('current_weather')).order_by('-date').values('avg_temp')[0].values())[0]

        my_obj = EmotionsAvgTemperature(date = date,
        joyfullness=joyfullness, average_temperature=average_temperature)        
        my_obj.save()  
    return render(request,'basic_app/emotions_form.html',{'form':form})



def emotions(request):
    # don't want to show to everyone, Login required

    emotions_list = Emotions.objects.all()
    context_dict = {'emotions_records':emotions_list}
    
    if request.method == 'POST':
        try:
            print(Emotions.objects.last().event)
            Emotions.objects.last().delete()

        except:
            print('No items to delete')
    return render(request,'basic_app/emotions.html', context = context_dict)

def login(request):
    return HttpResponse('Hello, from Login page')

def signup(request):
    return HttpResponse('Hello, from Sign up page')


def PieChart_Total():
    df = list(Emotions.objects.values('emotions').annotate(count = Count('emotions')).values('emotions','count'))
    values = []
    for row in df:
        my_list= [row['emotions'],row['count']]
        values.append(my_list)  
    values = eval(str(values).replace("'1'","'Страх'").replace("'2'","'Тоска'").replace("'3'","'Гнев'").replace("'4'","'Стыд'").replace("'5'","'Радость'"))
    return values

def PieChart_Today():
    df = list(Emotions.objects.values('emotions').filter(date__gte = datetime.date.today()).annotate(count = Count('emotions')).values('emotions','count'))
    values = []
    for row in df:
        my_list = [row['emotions'],row['count']]
        values.append(my_list)
    
    values = eval(str(values).replace("'1'","'Страх'").replace("'2'","'Тоска'").replace("'3'","'Гнев'").replace("'4'","'Стыд'").replace("'5'","'Радость'"))

    return values

def ScatterPlot(number):
    '''
    Function to calculate summary of fear and avg temp per day 
    by - group by day, calc avg and count
    and filter emotions - by type fear
    '''
    df = list(Emotions.objects.values('date').filter(emotions = number).annotate(avgTemp = Avg('current_weather'),
    count = Count('emotions')).order_by('date').values('avgTemp','count'))
    values = [[ 'Fear','Temperature']]

    for row in df:
        my_list = [row['count'], row['avgTemp']]
        values.append(my_list)

    with open("basic_app/static/scatter_fear.json", "w") as fp:
        json.dump(values , fp) 

    return values

def LineChart():
    '''
    Function to calculate avg temperature daily - group by day, calc avg of temp

    '''
    df = list(Emotions.objects.values('date').annotate(avgTemp = Avg('current_weather')).values('date','avgTemp'))
    values = [['year','value']]
    for row in df:
        my_list = [row['date'].strftime('%Y-%m-%d'),row['avgTemp']]
        values.append(my_list)
        with open('basic_app/static/avg_temp.json','w') as ft:
            json.dump(values,ft,sort_keys=True,
                                    indent=1,
                                    cls=DjangoJSONEncoder)
    return values

def HistogramChart():
    df = list(Emotions.objects.values('date').annotate(avgTemp = Avg('current_weather')))
    values = [['Date', 'Avg Temperature']]
    for row in df:
        my_list = [row['date'], row['avgTemp']]
        values.append(my_list)

    values = str(values).replace('datetime','"datetime').replace(')',')"')
    return values

def CalendarChart():
    df = list(Emotions.objects.values('date').annotate(avgTemp = Avg('current_weather')))
    values = []

    for row in df:
        my_list = [row['date'], row['avgTemp']]
        values.append(my_list)

    values = str(values).replace('datetime.date','new Date').replace('"','')
    return values

def BubbleChart():

    df = list(Emotions.objects.values('emotions_degree','emotions').annotate(avgTemp = Avg('current_weather'),
                                                                        countEm = Count('emotions_degree'),
                                                                        count = Count('emotions')).values('emotions_degree',
                                                                        'avgTemp','count','emotions','countEm'))
    values = [['Emotion Degree', 'Avg Temperature', 'Count of emotions', 'Emotions','Count of Emotions degree']]
    for row in df:
        my_list = [row['emotions_degree'],row['avgTemp'],row['count'],row['emotions'],row['countEm']]
        values.append(my_list)
        
    return values

def vis(request):
    # ----------------------- Data for Pie Chart Total -----------------------
    values = PieChart_Total()

    # -----------------------data for Pie Chart Current Day-----------------------

    val_pie_today = PieChart_Today() 
    # -----------------------data for DrawTable-----------------------
    table_values = [
                ['Курение',  3, 0],
                ['Все хорошо',   2, 1],
                ['Плохо по здоровью', 2,0],
                ['Плохая усидчивость',   0, 1]
                ]
    values_bad_dict = ['курить']
    queryset = Emotions.objects.filter(outcome__iregex=r'курила').values()

    # ----------------------- Data for line chart -----------------------   
    
    val_line = LineChart()

    # ----------------------- Data for Scatter Plot -----------------------
 
    val_scatter_joy =  ScatterPlot(5)
    val_scatter_fear = ScatterPlot(1)
    val_scatter_sadness = ScatterPlot(2)
    val_scatter_anger = ScatterPlot(3)
    val_scatter_shame = ScatterPlot(4)

    # ----------------------- Data for Histogram -----------------------

    val_hist = HistogramChart()

    # ----------------------- Data for Calendar -----------------------

    val_calendar = CalendarChart()
    # ----------------------- Data for Bubble -----------------------
    val_bubble = BubbleChart()

    return render(request,'basic_app/google_template.html', {'values':values,
                                                        'val_pie_today':val_pie_today,
                                                        'table_values':table_values,
                                                        'val_line':val_line,
                                                        'val_scatter_joy':val_scatter_joy,
                                                        'val_scatter_fear':val_scatter_fear,
                                                        'val_scatter_sadness': val_scatter_sadness,
                                                        'val_scatter_anger':val_scatter_anger,
                                                        'val_scatter_shame':val_scatter_shame,
                                                        'val_hist': val_hist,
                                                        'val_calendar':val_calendar,
                                                        'val_bubble':val_bubble
                                                        })

import pandas as pd
import yfinance as yf

def stocks(request):
    stocks_list = Stocks2.objects.order_by('-date').values()[:5] 
    import requests
    import json
    if request.method == 'POST':
        if 'searchTicker' in request.POST:
            ticker = request.POST['ticker']
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_3022547508644825871800589be99722")

            try:
                api = json.loads(api_request.content)
            except:
                api = "Error"
            return render(request,'basic_app/stocks.html',{'stocks_list':stocks_list,
                                                    'api':api})

        elif 'loadstocks' in request.POST:
            tickers_list = ['AAPL','TSLA']

            data = pd.DataFrame(columns=tickers_list)

            for ticker in tickers_list:
                data[ticker] = yf.download(ticker,datetime.date.today()-datetime.timedelta(2),
                datetime.date.today())['Adj Close']

            data = data.reset_index()
            data['Date2'] = pd.to_datetime(data['Date']).apply(lambda x: x.strftime('%Y-%m-%d'))

            date = data.loc[-1:,'Date2'][1]

            AAPL =data.loc[-1:,'AAPL'][1] 
            TSLA =data.loc[-1:,'TSLA'][1] 

            my_obj = Stocks2(date = date,AAPL=AAPL, TSLA=TSLA)        
            my_obj.save() 
        elif 'deletestocks' in request.POST:
            try:
                print(Stocks2.objects.last().date)
                Stocks2.objects.last().delete()
                stocks_list = Stocks2.objects.order_by('-date').values()[:5] 

            except:
                print('No items to delete')
    

    return render(request,'basic_app/stocks.html',{'stocks_list':stocks_list})

def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('basic_app:add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:

            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_3022547508644825871800589be99722")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except:
                api = "Error"
        return render(request,'basic_app/add_stock.html',{'ticker':ticker,'output':output})

def delete(request, stock_id):
    item = Stock.objects.get(pk = stock_id)
    item.delete()
    return redirect('basic_app:add_stock')

def about_me(request):

    if request.method == "POST":
        if 'about_me' in request.POST:
            form = TestForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('basic_app:about_me')
            else:
                return render(request,'basic_app/test_about_me.html')
        elif 'about_me_others' in request.POST:
            form = TestForm2(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('basic_app:about_me')
            else:
                return render(request,'basic_app/test_about_me.html')
        elif 'about_me_future' in request.POST:
            form = TestForm3(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('basic_app:about_me')
            else:
                return render(request,'basic_app/test_about_me.html')
        else:
            text = AboutMyView.objects.all()
            text2 = AboutMyViewOthers.objects.all()
            text3 = AboutMyViewFuture.objects.all()

            return render(request,'basic_app/test_about_me.html',{'text':text,'text2':text2,'text3':text3})
    else:

        text = AboutMyView.objects.all()
        text2 = AboutMyViewOthers.objects.all()
        text3 = AboutMyViewFuture.objects.all()

        return render(request,'basic_app/test_about_me.html',{'text':text,'text2':text2,'text3':text3})

def delete_about_me(request, text_id):
    item = AboutMyView.objects.get(pk = text_id)
    item.delete()
    return redirect('basic_app:about_me')

def delete_about_me_others(request, text_id):
    item = AboutMyViewOthers.objects.get(pk = text_id)
    item.delete()
    return redirect('basic_app:about_me')

def delete_about_me_future(request, text_id):
    item = AboutMyViewFuture.objects.get(pk = text_id)
    item.delete()
    return redirect('basic_app:about_me')





