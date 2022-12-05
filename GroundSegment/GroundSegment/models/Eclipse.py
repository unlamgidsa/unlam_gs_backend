'''
Created on Oct 4, 2017

@author: ubuntumate
'''
from datetime import datetime, timedelta
from django.db import models
import ephem
from GroundSegment.models.Satellite import Satellite

from GroundSegment.models.Sitio import Sitio
from GroundSegment.models.PassGeneration import PassGeneration
from django.db.models.deletion import CASCADE

class Eclipse(models.Model):
    startTime       = models.DateTimeField()
    stopTime        = models.DateTimeField()
    
    duration        = models.FloatField('Duracion', help_text='[minutos]', default=0.0)
    tleDistance     = models.FloatField("Fraccion de dias de distancia al TLE ", default=0)
    
    obsolete        = models.BooleanField(default=True)
    
    
    satellite       = models.ForeignKey(Satellite, related_name='eclipses', on_delete=CASCADE)
    tle             = models.ForeignKey('GroundSegment.Tle', related_name='eclipses', null=True, on_delete=CASCADE)
    
    
    def getStopTimeStr(self):
        return (datetime.strftime(self.stopTime,"%d %b %Y %H:%M:%S"))
        
    def getStartTimeStr(self):
        return (datetime.strftime(self.startTime,"%d %b %Y %H:%M:%S"))
    
    def __eq__(self, other):
        """
        ! NO SE USA ! SE FILTRA DIRECTAMENTE
        Cuando un eclipse es igual al otro?
        1.Cuando comparten nodo o en nuestro caso "satelite"
        2.Cuando sus tiempos de inicio y fin difieren en solo algunos 
        minutos. ¿Cuanto es algunos minutos? 
        """
        
        
        return  (other!=None) and \
                (self.satellite==other.satellite) and \
                (other.startTime-timedelta(minutes=5) <= self.startTime    <=  other.startTime+timedelta(minutes=5)) and \
                (other.stopTime-timedelta(minutes=5)  <= self.stopTime <=  other.stopTime+timedelta(minutes=5))    
    
    def getDuration(self):
        return (self.stopTime-self.startTime).total_seconds()
    
    def getDurationStr(self):
        """
        pasar la duracion de la pasada a un string que indique min:sec
        """
        intervalo=(self.stopTime-self.startTime).total_seconds()
        minutos = int(intervalo//60)
        segundos= int((intervalo % 60))

        return '%s:%s' % (str(minutos).zfill(2),str(segundos).zfill(2))#(self.stopTime-self.startTime)
    
    
    
    def save(self, *args, **kwargs):
        self.duration = self.getDuration()
        self.tleDistance = (self.startTime-self.tle.epoch).total_seconds()/86400
        
        super(Eclipse, self).save(*args, **kwargs)

    def __str__(self):
        return self.satellite.code+", "+str(self.startTime)+"-"+str(self.stopTime)

    
           

    