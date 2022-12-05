'''
Created on Feb 6, 2017

@author: ubuntumate
'''
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc


class Country(models.Model):
    code        = models.CharField('Codigo del Pais', max_length=24, unique=True)
    name        = models.CharField('Nombre del Pais', max_length=24, unique=True)
    description = models.CharField('Descripcion', max_length=24, unique=True)
    
    def __str__(self):
        return self.name