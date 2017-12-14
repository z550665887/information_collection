# Create your models here.
from django.db import models
import time
import datetime


class information(models.Model):
    information = models.TextField()
    IP = models.TextField()
    ID = models.IntegerField(primary_key=True,)
    timestamp =models.CharField(max_length=30,null=True)

class mysql(models.Model):
    information = models.TextField()
    IP = models.TextField()
    ID = models.IntegerField(primary_key=True,)