from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions
from basic_app.forms import FormEmotions
import requests
# Create your views here.


import random
import json
import os

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
    return render(request,'basic_app/emotions_form.html',{'form':form})



def emotions(request):
    # for e in Emotions.objects.all():
    #     print(e.event)
    emotions_list = Emotions.objects.all()
    context_dict = {'emotions_records':emotions_list,'insert_me':'Hello, I am from views'}
    
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
    # print(val_pie_today)
    # -----------------------data for DrawTable-----------------------
    table_values = [
                ['Курение',  3, 0],
                ['Все хорошо',   2, 1],
                ['Плохо по здоровью', 2,0],
                ['Плохая усидчивость',   0, 1]
                ]
    values_bad_dict = ['курить']
    
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
    # print((val_dict_str))
    
    return render(request,'basic_app/google_template.html', {'values':values,
                                                        'val_pie_today':val_pie_today,
                                                        'table_values':table_values,
                                                        'val_dict_str':val_dict_str})

