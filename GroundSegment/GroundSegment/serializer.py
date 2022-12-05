'''
Created on Jan 31, 2017

@author: ubuntumate
'''
from GroundSegment.models.DCPData import DCPData
from rest_framework.serializers import ModelSerializer

class DCPDataSerializer(ModelSerializer):
    class Meta:
        model = DCPData
        fields = ('dcp_plataform', 'Temp_max', 'Temp_media','Temp_min','Atm_preasure','Humidity','Precipitation')