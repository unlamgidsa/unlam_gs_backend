
'''
Created on Nov 16, 2016

@author: ubuntumate
'''


from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from django.db.models.query import QuerySet
import binascii
from django.utils import timezone
from django.db.models.deletion import CASCADE
from Telemetry.models.TlmyVarType import TlmyVarType
import pytz

class PredictionType(models.Model):
    code        = models.CharField('Code', max_length=24, help_text='', default="NoDef")
    description = models.CharField('Description', max_length=512, help_text='', default="NoDef") 
    aClass      = models.CharField('Class Name (Library)', max_length=512, help_text='', default="NoDef")
    

class TlmyPrediction(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    tlmyVarType = models.OneToOneField(TlmyVarType, on_delete=CASCADE, null=True)
    type        = models.ForeignKey(PredictionType, on_delete=CASCADE)
    updated     = models.DateTimeField()
    expiration  = models.DateTimeField()
    data        = models.BinaryField()
    std         = models.FloatField('Standard deviation', null=True)
    genTime     = models.FloatField('Calculate model time', default=0)
    
    def setData(self, s):
        self.data = s
        self.update = datetime.utcnow().replace(tzinfo=pytz.UTC)
    