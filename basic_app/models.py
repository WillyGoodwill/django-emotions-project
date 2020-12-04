from django.db import models
from django.utils import timezone
import datetime


class Emotions(models.Model):

    date = models.DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    currentweather = models.IntegerField(default =1.00 )
    event = models.CharField(max_length= 100)
    body_reaction = models.CharField(max_length= 100)
    thoughts = models.CharField(max_length= 100)
    outcome = models.CharField(max_length= 100)
    emotions = models.CharField(max_length= 100)
    emotions_degree = models.CharField(max_length= 100)


class MoodTracker(models.Model):
    mood = models.DecimalField(max_digits=11, decimal_places=4)
    datetime = models.DateTimeField()