'''
Created on Oct 6, 2017

@author: ubuntumate
'''
import numpy as np
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.DCPPlatform import DCPPlatform
from GroundSegment.models.Pasada import Pasada
from django.db.models.deletion import CASCADE

class TrackPoint(models.Model):
    epoch   = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pasada = models.ForeignKey(Pasada, on_delete=CASCADE, related_name="trackPoints")


    def getLatitudeInDegrees(self):
        return self.latitude*180.0/np.pi
    
    def getLongitudeInDegree(self):
        return self.longitude*180.0/np.pi