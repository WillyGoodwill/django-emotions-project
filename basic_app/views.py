from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions
from basic_app.forms import FormEmotions
import requests
# Create your views here.
# import os 

# from django.core.wsgi import get_wsgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emotions_project.settings")
# application = get_wsgi_application()
import random

def index(request):
    emotions_lib = ['радость','грусть','тоска','страх']
    value = random.choice(emotions_lib)
    if request.method == 'POST':
        value = random.choice(emotions_lib)
    return render(request,'basic_app/index.html',{'value':value})

def emotions_form(request):
    form = FormEmotions()
    if request.method == 'POST':
        form = FormEmotions(request.POST)
        if form.is_valid():
            form.save(commit = True)
            form = FormEmotions()
        else:
            print('Form invalid')
    return render(request,'basic_app/index.html',{'form':form})



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
    values =[
          ['Mushrooms', 3],
          ['Onions', 1],
          ['Olives', 1],
          ['Zucchini', 1],
          ['Pepperoni', 2]
        ]
    return render(request,'basic_app/google_template.html', {'values':values})


