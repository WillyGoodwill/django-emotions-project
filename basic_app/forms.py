from django import forms
from django.core import validators
from basic_app.models import Emotions
import datetime
from django.utils import timezone


class FormEmotions(forms.ModelForm):
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
    emotions = forms.CharField()
    body_reaction = forms.CharField()
    thoughts = forms.CharField()
    outcome = forms.CharField()

    class Meta():
        model = Emotions
        fields = '__all__'
        
    # botcatcher = forms.CharField(required = False,
    #                             widget =forms.HiddenInput,
    #                             validators = [validators.MaxLengthValidator(0)] )
    

        