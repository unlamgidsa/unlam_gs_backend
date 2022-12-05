'''
Created on Aug 24, 2016

@author: Pablo Soligo
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite
import ephem
from django.utils.timezone import datetime, now, timedelta, utc
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
import pytz
from django.db.models.deletion import PROTECT

#     created     = models.DateTimeField(editable=False)
#     modified    = models.DateTimeField()
# 
#     def save(self, *args, **kwargs):
#         #On save, update timestamps
#         if not self.id:
#             self.created = timezone.now()
#         self.modified = timezone.now()
#         return super(User, self).save(*args, **kwargs)
    

class Tle(models.Model):
    """
    Clase/Entidad TLE.
    Almacena la informacion de los TLE incluyendo su fecha de descarga y la epoca de TLE 
    """
    
    """
    Fecha generacion del TLE, si no fuera seteada se utilizara la fecha hora actual
    """
    tleDateTime = models.DateTimeField(auto_now_add=True)

    
    """
    Fecha de descarga del TLE
    """
    downloaded = models.DateTimeField(auto_now_add=True)
    
    
    lines = models.TextField(max_length=124, )
    
    """
    Epoca del TLE, es fundamental para saber si se esta trabajando con un TLE
    actualizado o es necesario descargar uno nuevo
    """
    
    epoch = models.DateTimeField("Epoca del TLE", null=True)
    """
    Lineas del TLE
    """
    
    validFrom  = models.DateTimeField("Fecha inicio desde donde aplicar TLE", null=True)
    validUntil = models.DateTimeField("Fecha hasta desde donde aplicar TLE", null=True)
    
    satellite = models.ForeignKey(Satellite, related_name='tles', on_delete=PROTECT)
    #latest() method
    """
    Satelite asociado al TLE
    """
    
    def getLine1(self):
        """
        Retorma la primera linea del TLE en formato texto plano
        @rtype:   string
        @return:  primera linea del TLE en texto plano.
        """

        
        return self.lines.split("\n")[0]
    
    
    def getLine2(self):
        """
        Retorma la segunda linea del TLE en formato texto plano
        @rtype:   string
        @return:  segunda linea del TLE en texto plano.
        """
        return self.lines.split("\n")[1]
    
    def getEpoch(self):
        
        
        if self.epoch==None:
            #Todavia no fue salvado
            
            #uso pyephem para extraer la fecha del tle
            etle =  twoline2rv(self.getLine1(), self.getLine2(), wgs72) 
            self.epoch = etle.epoch.replace(tzinfo=pytz.utc)
        
        return self.epoch
    
    def save(self):
        if self.epoch==None:
            #Todavia no fue salvado
            etle =  twoline2rv(self.getLine1(), self.getLine2(), wgs72) 
            self.epoch = etle.epoch.replace(tzinfo=pytz.utc)
            
        super(Tle, self).save()
        
    def __str__(self):
        return "Satellite: "+self.satellite.code+", epoch: "+str(self.getEpoch())
    
    
    def getAsEphemBody(self):
         
        localsat = ephem.readtle(self.satellite.code, self.getLine1(), self.getLine2()) 
        return localsat
        
        
        

        
    class Meta:
        get_latest_by = "tleDateTime"  
        
    