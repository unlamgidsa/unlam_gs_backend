'''
Created on 2 de dic. de 2016

@author: pabli
'''
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc


class Log(models.Model):
    """
    Entidad de log global de todo el sistema    
    """
    
    """
    Tipos de log, respeta la filosofia del event log del SO
    """
    INFORMATION     = 0
    WARNING         = 1
    ERROR           = 2
    
    LOGTYPE= (
        (INFORMATION, 'Information'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
        
    )
    
    @classmethod
    def create(cls, code, description, module, logType):
        log = cls()
        log.code = code
        log.description = description
        log.module = module
        log.logType = logType
        
        return log
    
    def __str__(self):
        return str(self.created)+", "+self.code 
    
    code           = models.CharField('Codigo del tipo de log', max_length=24, help_text='Codigo' )
    description    = models.TextField('Decripcion log', max_length=512, help_text='Decripcion del log')
    module         = models.CharField('Modulo', max_length=64, help_text='Modulo que genera el log' )
    logType        = models.IntegerField("Tipo de log", default=0, choices=LOGTYPE) 
    created        = models.DateTimeField(auto_now_add=True)
    