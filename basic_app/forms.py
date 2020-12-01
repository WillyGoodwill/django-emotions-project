from django import forms
from django.core import validators
from basic_app.models import Emotions

class FormEmotions(forms.ModelForm):
    date = forms.DateField()
    event = forms.CharField()
    emotions = forms.CharField()
    body_reaction = forms.CharField()
    thoughts = forms.CharField()
    outcome = forms.CharField()

    # botcatcher = forms.CharField(required = False,
    #                             widget =forms.HiddenInput,
    #                             validators = [validators.MaxLengthValidator(0)] )
    
    class Meta():
        model = Emotions
        fields = '__all__'
        