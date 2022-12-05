'''
Created on 22 de dic. de 2016

@author: pablsoligo
'''

from django.db import models
from .TlmyVarType import TlmyVarType
from django.db.models.deletion import PROTECT

class Coefficient(models.Model):
    code           = models.CharField('Codigo del coeficiente', max_length=24, help_text='Codigo del coeficiente')
    value          = models.FloatField(default=0.0)
    tlmyVarType    = models.ForeignKey(TlmyVarType, related_name="coefficients", on_delete=PROTECT)