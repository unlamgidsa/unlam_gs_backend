from django.db import models

# Create your models here.

from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc

from django.db.models.deletion import CASCADE
import ephem

class ReferenceSystem(models.Model):
    code           = models.CharField('Codigo del sistema de referencia', max_length=24, help_text='Codigo del sistema de referencia', unique=True)
    description    = models.CharField('Decripcion del sistema de referencia', max_length=100, help_text='Descripcion  del sistema de referencia', unique=True)
    


class Ephemeride(models.Model):
    #TODO falta modelo que indique el sistema de referencia
    
    x               = models.FloatField(help_text='vector posicion X',default=0.0)
    y               = models.FloatField(help_text='vector posicion Y',default=0.0)
    z               = models.FloatField(help_text='vector posicion Z',default=0.0)
    
    xp              = models.FloatField(help_text='vector velocidad X',default=0.0)
    yp              = models.FloatField(help_text='vector velocidad Y',default=0.0)
    zp              = models.FloatField(help_text='vector velocidad Z',default=0.0)
    
    epoch           = models.DateTimeField()
    satellite       = models.ForeignKey('GroundSegment.Satellite', on_delete=CASCADE, related_name='ephems')
    referenceSystem = models.ForeignKey(ReferenceSystem, on_delete=CASCADE, related_name='ephems')
    
    secondsInEclipse = models.IntegerField(help_text='Segundos en eclipse o tiempo restante para estarlo',null=True)
    eclipsed         = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.x) +","+ str(self.y) +","+ str(self.z) +"  "+ str(self.epoch) +" -> "+ self.satellite.code
    
    def __lookup_elapsedtime(self, sat_ephem):
        epoch = self.epoch
        result = 0
        
        extratime = 35

        if not self.eclipsed:
            sat_ephem.compute(self.epoch+timedelta(seconds=extratime))
            if (sat_ephem.eclipsed):
                #es una preumbra, calculo cuanto tiempo
                epoch = epoch+timedelta(seconds=1) 
                sat_ephem.compute(epoch)
                while(not sat_ephem.eclipsed):
                    epoch = epoch+timedelta(seconds=1) 
                    sat_ephem.compute(epoch)
                return extratime-(epoch-self.epoch).total_seconds()
            else:
                sat_ephem.compute(self.epoch+timedelta(seconds=-extratime))
                if (sat_ephem.eclipsed):
                    #Es una postumbra, calculo cuanto timpo
                    epoch = epoch+timedelta(seconds=-1) 
                    sat_ephem.compute(epoch)
                    while(not sat_ephem.eclipsed):
                        epoch = epoch+timedelta(seconds=-1) 
                        sat_ephem.compute(epoch)
                    
                    while(sat_ephem.eclipsed):
                        epoch = epoch+timedelta(seconds=-1) 
                        sat_ephem.compute(epoch)
                    
                    return (self.epoch-epoch).total_seconds()+extratime  
                else:
                    #no es ni preumbra ni postumbra, simplemente no esta eclipsado
                    #Cuanto falta para eclipse?   
                    epoch = epoch+timedelta(seconds=1) 
                    sat_ephem.compute(epoch)
                    while(not sat_ephem.eclipsed):
                        epoch = epoch+timedelta(seconds=1) 
                        sat_ephem.compute(epoch)
                        
                    return (self.epoch-epoch).total_seconds() + extratime
                    
           
             
                        
        else:
            #Eclipsado, hace cuanto tiempo?
            epoch = epoch+timedelta(seconds=-1) 
            sat_ephem.compute(epoch)
            while(sat_ephem.eclipsed):
                epoch = epoch+timedelta(seconds=-1) 
                sat_ephem.compute(epoch)
                
            return (self.epoch-epoch).total_seconds() + extratime
            
        
        
        """        
        if self.eclipsed and not self.umbra:
            while(sat_ephem.eclipsed):
                epoch = epoch+timedelta(seconds=-1) 
                sat_ephem.compute(epoch)
               
            result = (self.epoch-epoch).total_seconds()+umbrapost
        else:
            if self.umbra:
                while(not sat_ephem.eclipsed):
                    epoch = epoch+timedelta(seconds=-1) 
                    sat_ephem.compute(epoch)
                
                while(sat_ephem.eclipsed):
                    epoch = epoch+timedelta(seconds=-1) 
                    sat_ephem.compute(epoch)
                
                result = (self.epoch-epoch).total_seconds()
            else:
                while(not sat_ephem.eclipsed):            
                    epoch = epoch+timedelta(seconds=1) 
                    sat_ephem.compute(epoch)
                        
                result = -1*(epoch-self.epoch).total_seconds()+1
        return result
        """
    
    def save(self, *args, **kwargs):
        #Se puede calcular con x y z?
        
        tle=self.satellite.getTLE(self.epoch)
        
        if tle==None:
            raise Exception("TLE not available")
        
        sat_ephem = ephem.readtle(self.satellite.code, tle.getLine1(), tle.getLine2())
        
        
        sat_ephem.compute(self.epoch)
        self.eclipsed   = sat_ephem.eclipsed
        
               
        
        #Analizar situacion del eclipse
        if self.secondsInEclipse==None:
            self.secondsInEclipse = self.__lookup_elapsedtime(sat_ephem)
            #print("Se calculo->", self.epoch, self.secondsInEclipse)
        #if self.eclipsed:
        #    print("Eclipse calculado")
        
        
        #Calcular aca los segundos en eclipse
        #self.secondsInEclipse = 0;        
        super(Ephemeride, self).save(*args, **kwargs)
