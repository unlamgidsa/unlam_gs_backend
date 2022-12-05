'''
Created on Jan 30, 2017

@author: ubuntumate
'''

from django.db import models

from django.db.models.deletion import PROTECT

class FrameType(models.Model):
    aid           = models.IntegerField('id del tipo de paquete', help_text='id del tipo de paquete', unique=True)
    description  = models.CharField('Decripcion del tipo de paquete', max_length=100, help_text='Decripcion del tipo de paquete')
    satellite    = models.ForeignKey('GroundSegment.Satellite', related_name='framesTypes', null=True, on_delete=PROTECT)
    #odels.ForeignKey(UnitOfMeasurement, related_name="tlmyVarTypes", null=True, on_delete=PROTECT)
    
    def __str__(self):
        return str(self.id)+", "+self.description
    