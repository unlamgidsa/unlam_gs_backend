'''
Created on 4 de set. de 2016

@author: pabli
'''

from django.db import models
from GroundSegment.models.Alarm.Criticity import Criticity
from django.db.models.deletion import PROTECT



class AlarmType(models.Model):
    code            = models.CharField('Codigo del tipo de alarma', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description     = models.CharField('Decripcion del tipo de alarma', max_length=100, help_text='Decripcion del satelite', unique=True)
    
    criticity       = models.ForeignKey(Criticity, related_name='alarmstype', on_delete=PROTECT)
    procedure       = models.TextField(help_text='Procedimiento a ejecutar por los ingenieros de vuelo en caso de ocurrir alarma', max_length=512)
    
    timeout         = models.IntegerField(help_text='tiempo maximo para tratar la alarma', verbose_name='Tiempo maximo para tratar la alarma')
        
    def __str__(self):
        return self.code + ", " + self.description    
    
    
    def getAlarms(self):
        return self.alarms.all().count()
    
    
    
        