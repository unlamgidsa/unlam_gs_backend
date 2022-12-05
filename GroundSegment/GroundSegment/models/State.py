'''
Created on Feb 6, 2017

@author: ubuntumate
'''
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.Country import Country
from django.db.models.deletion import PROTECT

class State(models.Model):
    code        = models.CharField('Codigo del Estado', max_length=24, unique=True)
    name        = models.CharField('Nombre del Estado', max_length=24)
    description = models.CharField('Descripcion', max_length=24)
    country     = models.ForeignKey(Country,related_name='states', on_delete=PROTECT)
    
    def __str__(self):
        return self.name