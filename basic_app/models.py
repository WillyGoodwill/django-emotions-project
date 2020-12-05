from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Emotions(models.Model):

    date = models.DateField(auto_now=True)

    current_weather = models.FloatField(default=1)

    event = models.CharField(max_length= 100)
    emotions = models.CharField(max_length= 100)
    emotions_degree = models.CharField(max_length= 100)
    body_reaction = models.CharField(max_length= 100)
    thoughts = models.CharField(max_length= 100)
    outcome = models.CharField(max_length= 100)

