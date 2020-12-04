from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Emotions(models.Model):
    EMOTIONS_CHOICES = (
    (u'1', u'Страх'),
    (u'2', u'Тоска'),
    (u'3', u'Гнев'),
    (u'4', u'Стыд'),
    (u'5', u'Радость'),

)
    date = models.DateField(editable=True, auto_now=True)

    currentweather = models.FloatField(default = 1.0)

    event = models.CharField(max_length= 100)
    emotions = models.CharField(max_length= 100)
    # emotions = models.CharField(max_length=1, choices=EMOTIONS_CHOICES)
    body_reaction = models.CharField(max_length= 100)
    thoughts = models.CharField(max_length= 100)
    outcome = models.CharField(max_length= 100)

# class EmotionsDegree(models.Model):
#     emotions = models.ForeignKey(Emotions, on_delete = models.CASCADE)
#     if emotions == '':
#         degreeChoice1 = ['']
#     elif emotions == ''

#     # assign degree depending on choice
#     emotions_degree