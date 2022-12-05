'''
Created on Nov 16, 2016

@author: ubuntumate
'''


from sgp4.earth_gravity import wgs72
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc


from sgp4.io import twoline2rv
from GroundSegment.models.SatelliteState import SatelliteState


from django.db.models.query import QuerySet
import binascii
from django.utils import timezone
from django.db.models.deletion import CASCADE, PROTECT
from Telemetry.models.FrameType import FrameType

class TlmyRawData(models.Model):
    
    PENDING     = 0
    PROCESSED   = 1
    ABORTED     = 2
    
    RAWSTATE = (
        (PENDING, 'PENDING'),
        (PROCESSED, 'PROCESSED'),
        (ABORTED, 'ABORTED'),        
    )
    
    created         = models.DateTimeField(auto_now_add=True)
    capturedAt      = models.DateTimeField(default=datetime.strptime("1900-01-01 00:00:00", '%Y-%m-%d %H:%M:%S'))
    pktdatetime     = models.DateTimeField(default=datetime.strptime("1900-01-01 00:00:00", '%Y-%m-%d %H:%M:%S'))
    data            = models.BinaryField()
    #payload         = models.BinaryField(blank=True);
    
    pylStart        = models.IntegerField("Inicio de paquete de payload", default=0)
    pylEnd          = models.IntegerField("Fin del paquete de payload", default=0)
    
    
    #strpayload      = models.TextField("Payload data in text format", default='')
    #strdata         = models.TextField("Raw data in text format", default='')
    
    source          = models.CharField('Origen del dato, tipicamente cubesat/simulacion', max_length=24, help_text='Origen del dato, tipicamente cubesat/simulacion', default='simulation')
    dataLen         = models.IntegerField("Dimension del campo data, autoguardado", default=0)
    #processed      = models.BooleanField("Indica si el paquete raw fue procesado", default=False)
    state           = models.IntegerField("Estados, 0=Pending, 1=Processed, 2=Aborted", default=0, choices=RAWSTATE)    
    abortedError    = models.CharField('Error exception message', max_length=256, help_text='Error exception message', default='')
    
    processedTime   = models.FloatField("Tiempo en milisegundos que domoro en ser procesada", default=0.0)
    realTime        = models.BooleanField("Is the telemetry real time telemetry?", default=True)
    tag             = models.CharField("Free tag label", max_length=24, help_text='Free use', default='TEST')
    satellite       = models.ForeignKey('GroundSegment.Satellite', on_delete=CASCADE, related_name="rawdatas", default=1);     
    
    frameType       = models.ForeignKey(FrameType, related_name="raws", null=True, on_delete=PROTECT)
    
    
    class Meta:
        index_together = [
            ("satellite", "state"),
        ]
        #pktdatetime
        unique_together = ('pktdatetime', 'satellite',)
    
    def __getDataLen(self):
        #return self.data.nbytes
        return len(self.data)

    def saveToFile(self):
        blob = self.getBlob()
        f = open("tlmy-"+self.created.strftime("%Y%m%d-%H%M%S"), "wb")
        f.write(blob)
        f.close()

    
    def getPayloadBlob(self):
        #Se obtiene el payload del paquete de datos
        #return self.payload.tobytes()
        if self.pylEnd==0:
            return self.data
        else:
            return self.data[self.pylStart:self.pylEnd]

    
    def getBlob(self):
        #result = bytearray()
        #dl = len(self.data)#self.nbytes
        #for i in range(dl):
        #    result += self.data[i]
        #return result 
        return self.data
    
    def save(self, *args, **kwargs):
        
        #Deprecated
        #if len(self.data) == 0:
        #    self.data = binascii.unhexlify(self.strdata)
        
        #Deprecated
        #if len(self.payload) == 0:
        #    self.payload = binascii.unhexlify(self.strpayload)
        
        self.dataLen = self.__getDataLen()
        return super(TlmyRawData, self).save(*args, **kwargs)

    
    
    
"""  



def getBlobVectorSize(blobData):
    blobSize = unpack_from('!I',blobData, offset=4)
    return blobSize[0]

def readBlob(blobData):
    blobEncoding = unpack_from('!I',blobData, offset=0)
    formatStr = "!"

    if (blobEncoding[0] == 23):       #encoding vector<double> 

        vectorSize = getBlobVectorSize(blobData)       
        for x in range(0, vectorSize):
            formatStr += "d"

    else:
        raise ValueError("Unexpected blob encoding: %d" % blobEncoding[0])

    return getBlobVectorValues(blobData,formatStr)
    
"""

        