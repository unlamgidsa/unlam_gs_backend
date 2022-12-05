'''
Created on Jan 31, 2017

@author: ubuntumate
'''
from django.db import models
from django.db.models.deletion import CASCADE




class UnitOfMeasurement(models.Model):
    code           = models.CharField('Unidad de medida', help_text='Unidad de medida',max_length= 10 , unique = True)
    description    = models.CharField('Descripcion de Unidad de medida', max_length= 124 ,help_text='Descripcion de Unidad de medida')
    
    def __str__(self):
        return str(self.code)