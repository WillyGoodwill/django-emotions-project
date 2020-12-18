from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls.base import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
    with open(os.path.join(os.path.dirname(os.getcwd()),'emotions_project/basic_app/static/emotions_degree.json'), 'r') as json_file:

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

@login_required
def emotions_form(request):
    form = FormEmotions()
    if request.method == 'POST':
        form = FormEmotions(request.POST)
        if form.is_valid():
            newEmotions = form.save(commit = True)
            newEmotions.user = request.user
            newEmotions.save()
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
    if request.user.is_authenticated: 
        emotions_list = Emotions.objects.filter(user = request.user)
    else:
        emotions_list = 'You have no records'
    context_dict = {'emotions_records':emotions_list}
        
    if request.method == 'POST':
        try:
            print(Emotions.objects.last().event)
            Emotions.objects.last().delete()

        except:
            print('No items to delete')
    return render(request,'basic_app/emotions.html', context = context_dict)


def PieChart_Total(request):
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('emotions').annotate(count = Count('emotions')).values('emotions','count'))
        values = []
        for row in df:
            my_list= [row['emotions'],row['count']]
            values.append(my_list)  
        values = eval(str(values).replace("'1'","'Страх'").replace("'2'","'Тоска'").replace("'3'","'Гнев'").replace("'4'","'Стыд'").replace("'5'","'Радость'"))
    else:
        values = ''
    return values

def PieChart_Today(request):
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('emotions').filter(date__gte = datetime.date.today()).annotate(count = Count('emotions')).values('emotions','count'))
        values = []
        for row in df:
            my_list = [row['emotions'],row['count']]
            values.append(my_list)
        
        values = eval(str(values).replace("'1'","'Страх'").replace("'2'","'Тоска'").replace("'3'","'Гнев'").replace("'4'","'Стыд'").replace("'5'","'Радость'"))
    else:
        values = ''
    return values

def ScatterPlot(request,number):
    '''
    Function to calculate summary of fear and avg temp per day 
    by - group by day, calc avg and count
    and filter emotions - by type fear
    '''
    if request.user.is_authenticated:

        df = list(Emotions.objects.filter(user = request.user).values('date').filter(emotions = number).annotate(avgTemp = Avg('current_weather'),
        count = Count('emotions')).order_by('date').values('avgTemp','count'))
        values = [[ 'Fear','Temperature']]

        for row in df:
            my_list = [row['count'], row['avgTemp']]
            values.append(my_list)

        with open("basic_app/static/scatter_fear.json", "w") as fp:
            json.dump(values , fp) 
    else:
        values = ''

    return values

def LineChart(request):
    '''
    Function to calculate avg temperature daily - group by day, calc avg of temp

    '''
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('date').annotate(avgTemp = Avg('current_weather')).values('date','avgTemp'))
        values = [['year','value']]
        for row in df:
            my_list = [row['date'].strftime('%Y-%m-%d'),row['avgTemp']]
            values.append(my_list)
            with open('basic_app/static/avg_temp.json','w') as ft:
                json.dump(values,ft,sort_keys=True,
                                        indent=1,
                                        cls=DjangoJSONEncoder)
    else:
        values = ''
    
    return values

def HistogramChart(request):
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('date').annotate(avgTemp = Avg('current_weather')))
        values = [['Date', 'Avg Temperature']]
        for row in df:
            my_list = [row['date'], row['avgTemp']]
            values.append(my_list)

        values = str(values).replace('datetime','"datetime').replace(')',')"')
    else:
        values = ''

    return values

def CalendarChart(request):
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('date').annotate(avgTemp = Avg('current_weather')))
        values = []

        for row in df:
            my_list = [row['date'], row['avgTemp']]
            values.append(my_list)

        values = str(values).replace('datetime.date','new Date').replace('"','')
    else:
        values = ''

    return values

def BubbleChart(request):
    if request.user.is_authenticated:
        df = list(Emotions.objects.filter(user = request.user).values('emotions_degree','emotions').annotate(avgTemp = Avg('current_weather'),
                                                                            countEm = Count('emotions_degree'),
                                                                            count = Count('emotions')).values('emotions_degree',
                                                                            'avgTemp','count','emotions','countEm'))
        values = [['Emotion Degree', 'Avg Temperature', 'Count of emotions', 'Emotions','Count of Emotions degree']]
        for row in df:
            my_list = [row['emotions_degree'],row['avgTemp'],row['count'],row['emotions'],row['countEm']]
            values.append(my_list)
    else:
        values = ''
        
    return values

def vis(request):
    # ----------------------- Data for Pie Chart Total -----------------------
    values = PieChart_Total(request)

    # -----------------------data for Pie Chart Current Day-----------------------

    val_pie_today = PieChart_Today(request) 
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
    
    val_line = LineChart(request)

    # ----------------------- Data for Scatter Plot -----------------------
 
    val_scatter_joy =  ScatterPlot(request,5)
    val_scatter_fear = ScatterPlot(request,1)
    val_scatter_sadness = ScatterPlot(request,2)
    val_scatter_anger = ScatterPlot(request,3)
    val_scatter_shame = ScatterPlot(request,4)

    # ----------------------- Data for Histogram -----------------------

    val_hist = HistogramChart(request)

    # ----------------------- Data for Calendar -----------------------

    val_calendar = CalendarChart(request)
    # ----------------------- Data for Bubble -----------------------
    val_bubble = BubbleChart(request)
    if values=='' or val_pie_today == '':
        error = 'You have no records'
    else:
        error = ''

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
                                                        'val_bubble':val_bubble,
                                                        'error':error
                                                        })


@login_required
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
            if request.user.is_authenticated: 
                text = AboutMyView.objects.filter(user = request.user)
                text2 = AboutMyViewOthers.objects.filter(user = request.user)
                text3 = AboutMyViewFuture.objects.filter(user = request.user)
            else:
                text = 'No records'
                text2 = 'No records'
                text3 = 'No records'

            return render(request,'basic_app/test_about_me.html',{'text':text,'text2':text2,'text3':text3})
    else:
        if request.user.is_authenticated: 
            text = AboutMyView.objects.filter(user = request.user)
            text2 = AboutMyViewOthers.objects.filter(user = request.user)
            text3 = AboutMyViewFuture.objects.filter(user = request.user)
        else:
            text = 'No records'
            text2 = 'No records'
            text3 = 'No records'

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

def signupuser(request):
    if request.method=="GET":
        return render(request,'basic_app/signupuser.html',{'form':UserCreationForm()})
    else:
        # create a user
        if request.POST["password1"]==request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"],
                password = request.POST["password1"])
                user.save() # inserts into DB
                login(request,user) # logged in user
                return redirect('basic_app:index')
            except IntegrityError:
                return render(request,'basic_app/signupuser.html',{'form':UserCreationForm(),
                'error':'This user has already been chosen'})

        else:
            return render(request,'basic_app/signupuser.html',{'form':UserCreationForm(),
            'error':'Passwords did not match'})
@login_required
def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect('basic_app:index')
    return render(request,'basic_app/index.html')

def loginuser(request):
    if request.method=="GET":
        return render(request,'basic_app/loginuser.html',{'form':AuthenticationForm()})
    
    else:
        user = authenticate(request,username= request.POST["username"],password= request.POST["password"])
        if user is None:
            return render(request,'basic_app/loginuser.html',{'form':AuthenticationForm(),'error':'Username and password did not match'})
        else:
            login(request,user) # logged in user
            return redirect('basic_app:index')
