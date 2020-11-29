from django.db import models

# Create your models here.

class Emotions(models.Model):
    date = models.DateField()
    event = models.CharField(max_length= 100)
    emotions = models.CharField(max_length= 100)
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