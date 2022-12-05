'''
Created on 2 de dic. de 2016

@author: pabli
'''
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc


class Watchdog(models.Model):
    code           = models.CharField('Codigo del watchdog', max_length=24, help_text='Codigo' )
    description    = models.TextField('Decripcion watchdog', max_length=512, help_text='Decripcion del watchdog')
    module         = models.CharField('Modulo', max_length=64, help_text='Modulo que genera actualiza el watchdog' )
    lastUpdate     = models.DateTimeField(auto_now_add=True)
    tolerance      = models.FloatField('Tiempo de tolerancia')
    
    @classmethod
    def create(cls, code, description, module, tolerance):
        w = cls()
        w.code = code
        w.description = description
        w.module = module
        w.tolerance = tolerance
        return w
    
    def reset(self):
        self.lastUpdate = now()
        self.save()
        
    def isValid(self):
        #TODO
        pass