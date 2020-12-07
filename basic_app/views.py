from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions,EmotionsAvgTemperature
from basic_app.forms import FormEmotions,FormEmotionsAvgTemperature
import requests
# Create your views here.


import random
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

def vis(request):
    # ----------------------- Data for Pie Chart Total -----------------------
    try:
        fear = len(Emotions.objects.filter(emotions="1"))
    except:
        fear = 0
    try:
        sadness= len(Emotions.objects.filter(emotions="2"))
    except:
        sadness = 0
    try:
        anger= len(Emotions.objects.filter(emotions="3"))
    except:
        anger = 0
    try:
        shame = len(Emotions.objects.filter(emotions="4"))
    except:
        shame = 0
    try:
        joyfullness = len(Emotions.objects.filter(emotions="5"))
    except:
        joyfullness = 0

    values =[
            ['Страх', fear],
            ['Тоска', sadness],
            ['Гнев', anger],
            ['Стыд', shame],
            ['Радость', joyfullness]]
    # -----------------------data for Pie Chart Daily-----------------------

    emotions_array = ['Страх', 'Тоска', 'Гнев', 'Стыд', 'Радость']

    # iterate with if (== today date) append values
    import datetime
    values_pie = dict()
    for i,em in enumerate(emotions_array):
        # get date array for each emotion, sort 
        values_pie[em] = 0
        m = 0
        for j in range(len(Emotions.objects.all())):
            try:
                if Emotions.objects.all()[j].date == datetime.date.today() and Emotions.objects.all()[j].emotions == str(i+1): 
                    values_pie[em] = m+1
            except:
                values_pie[em] = 0 
    
    # transform to desired output {'fear':123,'sadness':123}
    values_str = str(values_pie)
    val_pie_today = eval(values_str.replace(',','],[').replace('{','[[').replace('}',']]').replace(':',','))
    print(val_pie_today)
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
    # grab unique dates
    date = []
    for i in range(len(Emotions.objects.all())):
        date.append(Emotions.objects.all()[i].date)

    date = sorted(list(set(date)))

    # create dictionary with array of temperatures for particular date
    val = dict()
    for j in date:
        val[j.strftime('%Y-%m-%d')]=[]
        for i in range(len(Emotions.objects.all())):
            if Emotions.objects.all()[i].date == j:
                val[j.strftime('%Y-%m-%d')].append(Emotions.objects.all()[i].current_weather)

    # calculate average for the day and save to dictionary by date key
    import statistics
    val_dict = dict()
    for j in date:
        val_dict[j.strftime('%Y-%m-%d')]=[]
        val_dict[j.strftime('%Y-%m-%d')].append(statistics.mean(val[j.strftime('%Y-%m-%d')]))

    # regexp to remove [] and replace : with ,
    val_dict_str = str(val_dict)
    val_dict_str = val_dict_str.replace('[','').replace(']','').replace(',','],[').replace(':',',').replace('{','[').replace('}',']')
    # eval(val_dict_str) to get back normal array
    val_dict_str = [['year','value'],eval(val_dict_str)]
    val_dict_str = str(val_dict_str)
    val_dict_str = val_dict_str.replace('(','').replace(')','')
    val_dict_str = eval(val_dict_str)
    print((val_dict_str))
    
    # ----------------------- Data for Scatter Plot -----------------------
    # NEED:Summary of Joyfullness per day
    # filter joyfullness
    import pandas as pd
    import datetime
    # filter emotions - by type Joyfullness
    df = pd.DataFrame(list(Emotions.objects.all().filter(emotions ='5').values()))
    # df = pd.DataFrame(list(Emotions.objects.all().filter(date__gte =datetime.date.today()).values()))
    df1 = df.groupby('date').count()[['id']]
    df1 = df1.rename(columns = {'id':'count_of_joy'})
    df2 = df.groupby('date').mean()[['current_weather']]
    df3 = df1.join(df2)
    val_scatter = [[ 'Joyfullness','Temperature']]

    for index,row in df3.iterrows():
        my_list =[row.count_of_joy,row.current_weather]
        val_scatter.append(my_list)

    print(val_scatter)
    # convert to pandas dataframe
    # accumulate group by date with count

    return render(request,'basic_app/google_template.html', {'values':values,
                                                        'val_pie_today':val_pie_today,
                                                        'table_values':table_values,
                                                        'val_dict_str':val_dict_str,
                                                        'val_scatter':val_scatter
                                                        })

