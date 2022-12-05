'''
Created on Aug 29, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Propagation import Propagation
import math
from django.db.models.deletion import PROTECT, CASCADE

class PropagationDetail(models.Model):
    created     = models.DateTimeField(auto_now_add=True)    
    dt          = models.DateTimeField()
    propagation = models.ForeignKey(Propagation, related_name='propagationDetails', on_delete=CASCADE)
    
    positionX = models.FloatField()
    positionY = models.FloatField()
    positionZ = models.FloatField()
    
    velocityX = models.FloatField()
    velocityY = models.FloatField()
    velocityZ = models.FloatField()
    
    earthDistance = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.earthDistance = math.sqrt(self.positionX**2+self.positionY**2+self.positionZ**2)
        super(PropagationDetail, self).save(*args, **kwargs)
    