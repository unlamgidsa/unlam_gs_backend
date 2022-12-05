'''
Created on Jan 25, 2017

@author: ubuntumate
'''
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.Sitio import Sitio
from django.db.models.deletion import CASCADE


class DCPPlatform(models.Model):
    code        = models.CharField('Codigo de la Plataforma', max_length=24, unique=True)
    
    
    sitio       = models.ForeignKey(Sitio,related_name='dcpplatform', null=True, on_delete=CASCADE)
    type        = models.CharField('Tipo de Plataforma', max_length=24, null=True)
    equip_marca = models.CharField('Marca del Equipo', max_length=24, null=True, default='no conocido')
    equip_model = models.CharField('Modelo del Equipo', max_length=24, null=True, default='no conocido')

    def __str__(self):
        return self.code
    
    def setData(self, datetime,  precipitation, humidity, temp_max, temp_media, temp_min, atm_preasure):
        #TODO, poner datos en tiempo real en esta entidad y utilizar setData para guardar historicos
        #y setear tiempo real, por ahora solo tiempo real
        from GroundSegment.models.DCPData import DCPData
        dspData = DCPData()
        dspData.dcp_plataform   = self
        dspData.dataTime        = datetime
        dspData.receive_dataTime= utc
 #       dspData.snow            = snow
        dspData.Precipitation   = precipitation
 #       dspData.Temperature     = temperature
        dspData.Humidity        = humidity
 #       dspData.Wind_dir        = windDir
 #       dspData.Wind_speed      = windSpeed
 #       dspData.Bat_volts       = batVolt
 #       dspData.cm_data         = cmData
        dspData.Temp_max        = temp_max
        dspData.Temp_media      = temp_media
        dspData.Temp_min        = temp_min
        dspData.Atm_preasure    = atm_preasure
        dspData.save()
        
        return dspData
        
        