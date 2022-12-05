'''
Created on 26 de nov. de 2016

@author: pabli
'''

from django.db import models
from GroundSegment.models.SubSystem import SubSystem
from django.db.models.deletion import PROTECT


class Calibration(models.Model):
    aClass  = models.CharField('Clase donde se encuentra la funcion de calibracion', max_length=128, help_text='Clase donde se encuentra la funcion de calibracion')
    aMethod = models.CharField('Metodo de calibracion', max_length=128, help_text='Metodo de calibracion')
    subsystem = models.ForeignKey(SubSystem, on_delete=PROTECT, related_name="calibrations")
    
    def __str__(self):
        return self.subsystem.code+", "+self.aClass+", "+self.aMethod