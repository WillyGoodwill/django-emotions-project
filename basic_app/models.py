from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Emotions(models.Model):

    date = models.DateField(editable=True, auto_now=True)

    currentweather = models.FloatField(default = 1.0)

    event = models.CharField(max_length= 100)
    emotions = models.CharField(max_length= 100)
    emotions_degree = models.CharField(max_length= 100,default = 1)

    # emotions = models.CharField(max_length=1, choices=EMOTIONS_CHOICES)
    body_reaction = models.CharField(max_length= 100)
    thoughts = models.CharField(max_length= 100)
    outcome = models.CharField(max_length= 100)

