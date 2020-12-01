from django.shortcuts import render
from django.http import HttpResponse

from basic_app.models import Emotions
from basic_app.forms import FormEmotions

# Create your views here.
# import os 

# from django.core.wsgi import get_wsgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emotions_project.settings")
# application = get_wsgi_application()

def index(request):
    return render(request,'basic_app/index.html')

def emotions_form(request):
    
    form = FormEmotions()
    
    if request.method == 'POST':
        form = FormEmotions(request.POST)
        if form.is_valid():
            form.save(commit = True)
            form = FormEmotions()
        else:
            print('Form invalid')
    return render(request,'basic_app/form_page.html',{'form':form})


def emotions(request):
    # for e in Emotions.objects.all():
    #     print(e.event)
    emotions_list = Emotions.objects.all()
    context_dict = {'emotions_records':emotions_list,'insert_me':'Hello, I am from views'}
    return render(request,'basic_app/emotions.html', context = context_dict)

def login(request):
        return HttpResponse('Hello, from Login page')

def signup(request):
        return HttpResponse('Hello, from Sign up page')


