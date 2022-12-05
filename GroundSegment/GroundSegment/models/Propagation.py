'''
Created on Aug 29, 2016

@author: ubuntumate
'''

from django.db import models

from GroundSegment.models.Tle import Tle
from GroundSegment.models.Satellite import Satellite
from django.db.models.deletion import PROTECT

class Propagation(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    tle         = models.ForeignKey(Tle, related_name='propagations', on_delete=PROTECT)

    satellite   = models.ForeignKey(Satellite, related_name='propagations', on_delete=PROTECT)
    final       = models.BooleanField(default = False)