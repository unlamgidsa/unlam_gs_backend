'''
Created on 3 de dic. de 2016

@author: pabli
'''
from django.db import models


class PacketType(models.Model):
    code           = models.CharField('Codigo del tipo de paquete', max_length=24, help_text='Codigo del tipo de paquete', unique=True)
    description    = models.CharField('Decripcion del tipo de paquete', max_length=100, help_text='Decripcion del tipo de paquete')
    