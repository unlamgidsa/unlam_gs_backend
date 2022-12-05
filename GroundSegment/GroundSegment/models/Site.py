'''
Created on Sep 16, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite
from _datetime import datetime, timedelta
from django.utils.timezone import utc
from GroundSegment.Utils.UtilsFunctions import *
#from GroundSegment.models.Satellite import Satellite
#from django.contrib.admin.utils import help_text_for_field
"""

class Site(models.Model):
    name        = models.CharField("Nombre del Sitio", max_length=100, unique=True)
    latitude    = models.FloatField('latitude', help_text='[Grados Decimales]')
    longitude   = models.FloatField('Longitud', help_text='[Grados Decimales]')
    altitude    = models.FloatField('altura', help_text='[metros]')
    
    def setLatitude(self, value):
        #Meter proteccion
        self.latitude = value
        
    def setLongitude(self, value):
        #Meter proteccion
        self.longitude = value
    
    def setAltitude(self, value):
        #Meter proteccion
        self.altitude = value

    def getPass(self, fro, to, satellite):
        #hacer todos los calculos
        import ephem;
        
        #from calendar import timegm
        
        #Remplazar site por el sitio, entidad no creada aun
        
        tle = satellite.getLastTLE()
        
        sat = ephem.readtle(satellite.code, tle.getLine1(), tle.getLine2())
        
        #iss = ephem.readtle(line1, line2, line3)
        #iss.compute('2003/3/23')
        
        ifro = ephem.Date(fro)
        ito = ephem.Date(to)
        
        site = ephem.Observer()
        site.lon = str( self.longitude )
        site.lat = str( self.latitude )
        site.elevation = self.altitude
        site.name = self.name
        site.date = ifro
        site.epoch = ifro
        
        #while ifro < ito:   
        while site.date < ito:
            sat.compute(site)
            tr, azr, tt, altt, ts, azs = site.next_pass(sat)
            
            duration    = int((ts - tr) *60*60*24)
            rise_time   = datetime_from_time(tr)
            max_time    = datetime_from_time(tt)
            set_time    = datetime_from_time(ts)
            
            site.date = rise_time + timedelta(seconds=duration)
            print('Date:', site.date, "rise_time ", rise_time, "set_time ", set_time)   
                
            
        
        return None

        #site.date = 
        #site.next_transit(esat)
        #site.next_rising(esat)
        
        #Faltaria filtrar por fechas!!, investigar como hacer y pelearla, con un ejemplo nos alcanza para todo
        #el proyecto
        #pd = PropagationDetail.objects.filter(propagation__satellite=Satellite, )
        
        #if pd.count()!=(fro-to).total_seconds():
            #El detalle de propagacion no coincide con el total buscado, por tanto se requiere propagar los faltantes
        
        #Se imprime los detalles de propagacion del satellite solo como muestra, quitar el print
        
        #for pr in pd:
        #    print(pr.positionX, pr.positionY, pr.positionZ)
        
      
"""        
       
       
