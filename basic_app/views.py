from django.shortcuts import render

from basic_app.models import Emotions


# Create your views here.
import os 
from django.core.wsgi import get_wsgi_application
from basic_app.models import Emotions
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emotions_project.settings")
application = get_wsgi_application()

def index(request):

    return render(request,'basic_app/index.html')

def emotions(request):
    for e in Emotions.objects.all():
        print(e.event)
    emotions_list = Emotions.objects.all()
    context_dict = {'emotions_records':emotions_list,'insert_me':'Hello, I am from views'}
    return render(request,'basic_app/emotions.html', context = context_dict)
