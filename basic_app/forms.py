from django import forms
from django.core import validators
from basic_app.models import Emotions, EmotionsAvgTemperature,Stocks2
import datetime
from django.utils import timezone
import os
import json
import requests


class FormEmotions(forms.ModelForm):
    # emotions list
    EMOTIONS_CHOICES = (
    (u'1', u'Страх'),
    (u'2', u'Тоска'),
    (u'3', u'Гнев'),
    (u'4', u'Стыд'),
    (u'5', u'Радость'))
    
    # emotions degree list
    with open(os.path.join(os.path.dirname(os.getcwd()),'emotions_project/templates/basic_app/emotions_degree.json'), 'r') as json_file:
        data1 = json.load(json_file)
        data2 = data1[0]['Страх'] + data1[0]['Тоска'] + data1[0]['Гнев']+ data1[0]['Стыд']+ data1[0]['Радость']
        data3 = tuple([(k, v) for k,v in enumerate(data2)])

    
    # getting current weather from API for St. Petersburg
    import requests
    import json 
    appid = "e39c82d8879b82213e1312de1f211aa5"
    city_id = 498817    
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    current_weather_temp = data['main']['temp']
    # other fields
    date = forms.DateField(initial = timezone.now())
    current_weather = forms.FloatField(initial = current_weather_temp, required=False)
    event = forms.CharField(required = False)

    emotions = forms.ChoiceField(choices = EMOTIONS_CHOICES)

    emotions_degree = forms.ChoiceField(choices = data3)

    body_reaction = forms.CharField(required = False)
    thoughts = forms.CharField(required = False)
    outcome = forms.CharField(required = False)

    class Meta():
        model = Emotions
        fields = '__all__'
        
    # botcatcher = forms.CharField(required = False,
    #                             widget =forms.HiddenInput,
    #                             validators = [validators.MaxLengthValidator(0)] )
    
class FormEmotionsAvgTemperature(forms.ModelForm):
    date = forms.DateField()
    joyfullness = forms.FloatField(required = False)
    average_temperature = forms.FloatField(required = False)

class FormStocks2(forms.ModelForm):
    date = forms.DateField() 
    AAPL = forms.FloatField(required = False)
    TSLA = forms.FloatField(required = False)