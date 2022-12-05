'''
Created on 25 de ago. de 2016

@author: pabli
'''

from django.db import models



class SatelliteState(models.Model):
    code           = models.CharField('Codigo de estado', max_length=24, help_text='Codigo de estado del satelite', unique=True)
    description    = models.CharField('Codigo de estado', max_length=100, help_text='Decripcion del estado del satelite', unique=True)
    
    def __str__(self):
        return self.code