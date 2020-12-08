from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions,EmotionsAvgTemperature
from basic_app.forms import FormEmotions,FormEmotionsAvgTemperature
import requests
# Create your views here.


import random
from django.core.serializers.json import DjangoJSONEncoder
import json

import os
import pandas as pd
import datetime

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
    # for e in Emotions.objects.all():
    #     print(e.event)
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

def ScatterPlot_Joyfullness():
    '''
    Function to calculate summary of Joyfullness and avg temp per day 
    by - group by day, calc avg and count
    and filter emotions - by type Joyfullness
    '''
    df = list(Emotions.objects.values('date').filter(emotions = '5').annotate(avgTemp = Avg('current_weather'),
    count = Count('emotions')).order_by('date').values('avgTemp','count'))
    values = [[ 'Joyfullness','Temperature']]

    for row in df:
        my_list = [row['count'], row['avgTemp']]
        values.append(my_list)

    with open("basic_app/static/scatter_joyfullness.json", "w") as fp:
        json.dump(values , fp) 

    return values

def ScatterPlot_Fear():
    '''
    Function to calculate summary of fear and avg temp per day 
    by - group by day, calc avg and count
    and filter emotions - by type fear
    '''
    df = list(Emotions.objects.values('date').filter(emotions = '1').annotate(avgTemp = Avg('current_weather'),
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
 
    val_scatter_joy =  ScatterPlot_Joyfullness()
    val_scatter_fear = ScatterPlot_Fear()

    # ----------------------- Data for Histogram -----------------------

    val_hist = HistogramChart()

    # ----------------------- Data for Calendar -----------------------

    val_calendar = CalendarChart()

    return render(request,'basic_app/google_template.html', {'values':values,
                                                        'val_pie_today':val_pie_today,
                                                        'table_values':table_values,
                                                        'val_line':val_line,
                                                        'val_scatter_joy':val_scatter_joy,
                                                        'val_scatter_fear':val_scatter_fear,
                                                        'val_hist': val_hist,
                                                        'val_calendar':val_calendar
                                                        })

