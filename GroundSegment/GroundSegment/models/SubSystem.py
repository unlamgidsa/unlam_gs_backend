'''
Created on 26 de nov. de 2016

@author: pabli
'''



from django.db import models


class SubSystem(models.Model):
    code           = models.CharField('Codigo del subsistema', max_length=24, help_text='Codigo del subsistema', unique=True)
    description    = models.CharField('Decripcion del subsistema', max_length=100, help_text='Decripcion del subsistema', unique=True)
    
    
    def __str__(self):
        return self.code