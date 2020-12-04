from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions, MoodTracker
from basic_app.forms import FormEmotions

# Create your views here.
# import os 

# from django.core.wsgi import get_wsgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emotions_project.settings")
# application = get_wsgi_application()

def index(request):
    form = FormEmotions()
    if request.method == 'POST':
        form = FormEmotions(request.POST)
        if form.is_valid():
            form.save(commit = True)
            form = FormEmotions()
        else:
            print('Form invalid')
    return render(request,'basic_app/index.html',{'form':form})

# def emotions_form(request):
    
#     form = FormEmotions()
    
#     if request.method == 'POST':
#         form = FormEmotions(request.POST)
#         if form.is_valid():
#             form.save(commit = True)
#             form = FormEmotions()
#         else:
#             print('Form invalid')
#     return render(request,'basic_app/form_page.html',{'form':form})


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


# from qsstats import QuerySetStats
# from qsstats import Count
import datetime
def vis(request):
    # start_date = datetime.datetime(1980, 5, 8, 00, 00).date()
    # end_date = datetime.datetime(2020, 5, 8, 00, 00).date()

    # queryset = MoodTracker.objects.all()
    # # считаем количество платежей...
    # qsstats = QuerySetStats(queryset, date_field='datetime', aggregate = Count('id'))

    # ...в день за указанный период
    # values = qsstats.time_series(start_date, end_date, interval='days')

    # summary = qsstats.time_series(start_date, end_date, interval='days', aggregate = Count('id'))
    values = ([
                ['Страх', 3],
                ['Тоска', 1],
                ['Грусть', 1],
                ['Радость', 2]
            ])
    values2 =[
                    ["Element", "Density"],
                    ["Copper", 8.94],
                    ["Silver", 10.49],
                    ["Gold", 19.30],
                    ["Platinum", 21.45]
                ]
    return render(request,'basic_app/google_template.html', {'values': values,'values2': values2})

