'''
Created on 25 de ago. de 2016

@author: pablosoligo
'''

from django.db import models
from .CommandType import CommandType
from django.db.models.deletion import CASCADE


class CommandTypeParameter(models.Model):
    code           = models.CharField('Codigo del parametro', max_length=24, help_text='Codigo del parametro', default="NoDet")
    description    = models.CharField('Decripcion del parametro', max_length=100, help_text='Decripcion del satelite', default="NoDet")
    commandType    = models.ForeignKey(CommandType, on_delete=CASCADE, related_name="parameters", null=True)
    position       = models.IntegerField(default=0)
    valueMin     = models.FloatField(default=0.0)
    valueMax     = models.FloatField(default=0.0)
     
    def __str__(self):
        return self.code
    