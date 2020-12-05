from django import forms
from django.core import validators
from basic_app.models import Emotions
import datetime
from django.utils import timezone


class FormEmotions(forms.ModelForm):
    
    EMOTIONS_CHOICES = (
    (u'1', u'Страх'),
    (u'2', u'Тоска'),
    (u'3', u'Гнев'),
    (u'4', u'Стыд'),
    (u'5', u'Радость'))

    
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
    currentweather = forms.FloatField(initial = current_weather_temp, required=False)
    event = forms.CharField()

    emotions = forms.ChoiceField(choices = EMOTIONS_CHOICES)

    emotions_degree = forms.MultipleChoiceField(choices = EMOTIONS_CHOICES,widget=forms.CheckboxSelectMultiple)

    body_reaction = forms.CharField()
    thoughts = forms.CharField()
    outcome = forms.CharField()

    class Meta():
        model = Emotions
        fields = '__all__'
        
    # botcatcher = forms.CharField(required = False,
    #                             widget =forms.HiddenInput,
    #                             validators = [validators.MaxLengthValidator(0)] )
    

        