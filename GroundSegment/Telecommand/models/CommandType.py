'''
Created on 25 de ago. de 2016

@author: pabli
'''

from django.db import models
from django.utils.timezone import datetime, now, timedelta
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from django.db.models.deletion import PROTECT





class CommandType(models.Model):
    code           = models.CharField('Codigo del tipo de comando', max_length=24, help_text='Codigo del tipo de comando', unique=True)
    description    = models.CharField('Decripcion del tipo de comando', max_length=100, help_text='Decripcion del tipo de comando', unique=True)
    satellite      = models.ForeignKey(Satellite, related_name='commandsType', on_delete=PROTECT)
    satelliteStates= models.ManyToManyField(SatelliteState, related_name='commandsType')
    active         = models.BooleanField(default=True)
    transactional  = models.BooleanField(default=False) 
    timeout        = models.IntegerField('Tiempo en segundos?', default=0, null=False) 
    notes          = models.TextField('Consecuencias, restricciones del comando', max_length=512, null=True)
    maxRetry       = models.IntegerField(default=2)
    
    commandCode    = models.CharField('Codigo de comando segun el satelite, por ejemplo para isis cubesat telemetryEPS->23', max_length=24, default='0')
    
    
    @classmethod
    def create(cls, code, description, satellite, satelliteState, transactional, timeout, notes, maxRetry, commandCode):
        result = cls()
        result.code             = code
        result.description      = description
        result.satellite        = satellite
        result.satelliteState   = satelliteState
        result.transactional    = transactional
        result.timeout          = timeout
        result.notes            = notes
        result.maxRetry         = maxRetry
        result.commandCode      = commandCode
        
        return result
    
    """
    #@classmethod
    def newCommand(self, satellite, expiration):
        from .Command import Command
        result = Command()
        
        if satellite!=self.satellite:
            raise Exception("Este tipo de comando no puede ser aplicado al satelite pasado como parametro")
        
        result.satellite    = satellite
        result.commandType  = self
        result.created      = now()
        result.sent         = None
        result.retry        = 0
        result.expiration   = expiration
        #Mejorar la forma en que se trabajan las enumeraciones!
        result.state        = 0
        
        return result
    """
    
    def __str__(self):
        return self.code
    