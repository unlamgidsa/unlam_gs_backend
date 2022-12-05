'''
Created on Oct 27, 2016

@author: ubuntumate
'''

from xmlrpc.client import boolean
from django.db import models
from GroundSegment.models.Alarm.Alarm import Alarm
from django.utils.timezone import datetime, now, timedelta, utc
from django.utils import timezone
#TODO Estos tienen que figurar aca...verificar de hacer la carga dinamica
from django.db.models.deletion import PROTECT
from Telemetry.models.TlmyRawData import TlmyRawData
from Calibration import *
from .TlmyVarType import TlmyVarType
from TlmyCmdProcessor.TlmyCmdProcessor import is_set
from struct import unpack
import json
import django.dispatch
from django.core.serializers import serialize
from django.utils import timezone
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

before_bulk_create = django.dispatch.Signal()



"""

class TlmyLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, TlmyVar):
            return obj.toJson()
        return super().default(obj)
"""


"""
class PTlmyVar():
    def __init__(self, code, calSValue, tstamp, UnixTimeStamp, fullname):

        self.code               = code
        self.calSValue          = calSValue
        self.tstamp             = tstamp
        self.UnixTimeStamp      = UnixTimeStamp
        self.fullName           = fullname
"""


class TlmyVarManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        #Pasar a asincrono para informar en tiempo totalmente real  
        #objs es lista de objetos django, convierto a objetos planos
        try:
            #for test (before bulk create) pourpose
            dt = timezone.now()
            for o in objs:
                o.created = dt
            
            jsonObjs = self.__dObjsToJson(objs)
            #jsonObjs = serializers.serialize('json', list(objs), fields=('id','code','calSValue', 'UnixTimeStamp', 'created'))

            """
            channel_layer = get_channel_layer()
            tlmys = jsonObjs
            channel_layer.group_send(
                    "RTTelemetry", #esto seria el room.group_name 
                    {
                        "type": "onNewtlmy", #Function name!
                        "tlmyVars": tlmys,                
                    }
                )
            """


            #print("Se envia signal, tiempo de serializacion:", (timezone.now()-dt).total_seconds())
            before_bulk_create.send(sender=self.__class__, tlmys=jsonObjs)
            #print("Signal enviada")
        except Exception as ex:
            print("Send signal error ", str(ex))

        print("Bulk create a ejecutar")
        #Comentado temporalmente
        #bcr = super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
        #return bcr 
        print("Bulk create exitoso")
        return None
        


       
    
    
    
    def __dObjsToJson(sender, objs):
        
        result = []
        #if len(objs)>0:
        #    arrive_time = o.tlmyRawData.createdAt
        for o in objs:
            result.append({ 'id':o.id,
                            'code':o.code, 
                            'calSValue':o.calSValue, 
                            #"tstamp:": o.tstamp,
                            'UnixTimeStamp:':o.UnixTimeStamp,
                            'created':o.created.isoformat(),
                            'fullName': o.getFullName()})

        return json.dumps(result)
        
        


    #async def asyncBulkCreate(self, objs):
    #    await super().bulk_create(objs)

    def __del__(self):
        pass
        before_bulk_create.disconnect()
       

class TlmyVar(models.Model):
    
    objects     = TlmyVarManager() 
    code        = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo de la variable, se quita relacion con maestro', default="NoDef")
    #rawValue    = models.BigIntegerField(default=0)
    rawValue    = models.BinaryField(null=True)

    calIValue   = models.BigIntegerField(default=0)
    calFValue   = models.FloatField(default=0.0)
    calBValue   = models.BooleanField(default=False)
    calSValue   = models.CharField('Valor como string de la variable de telemetria', default=None, max_length=24, help_text='Valor como string de la variable de telemetria')
        
    created         = models.DateTimeField(auto_now_add=True)
    tstamp          = models.DateTimeField(default=datetime.strptime("1976-10-30 12:00:00", '%Y-%m-%d %H:%M:%S'))
    UnixTimeStamp   = models.FloatField(default=0.0) #db_index=True, se quita el indice, se trabaja directamente con unixtimestamp
    
    
    outlier     = models.BooleanField("Valor erroneo", default=False)
    #created     = models.DateTimeField()
    #Quito la relacion para que no me obligue a guardar el padre
    #para despues guardar al hijo
    tlmyVarType = models.ForeignKey(TlmyVarType, related_name="tlmyVars", on_delete=PROTECT)
    tlmyRawData = models.ForeignKey(TlmyRawData, on_delete=PROTECT, related_name='tlmyVars', null=True)
    #satellite   = models.ForeignKey('GroundSegment.Satellite', related_name="tlmyvars", on_delete=PROTECT)
    @property
    def fullName(self):
        return self.tlmyVarType.fullName

    class Meta:
    
        #index_together = [
        #    ("satellite", "state"),
        #]
        
        unique_together = ('tlmyVarType', 'tstamp',)
        
    


    def getValue(self):
        #Retorna el valor en funcion del tipo
        #Comenzar a usar type
        
        if self.tlmyVarType.ctype.varType==self.tlmyVarType.ctype.INTEGER:
            return self.calIValue
        elif self.tlmyVarType.ctype.varType==self.tlmyVarType.ctype.FLOAT:
            return self.calFValue
        elif self.tlmyVarType.ctype.varType==self.tlmyVarType.ctype.BOOLEAN:
            return self.calBValue        
        else:
            return self.calSValue
        
        
    def getPredictedValue(self):
        if hasattr(self, 'info'):
            if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
                return int(self.info.calSPredictedValue)
            elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
                return float(self.info.calSPredictedValue)
            elif self.tlmyVarType.varType==self.tlmyVarType.BOOLEAN:
                return bool(self.info.calSPredictedValue)      
            else:
                return self.calSPredictedValue
        else:
            return None
      
    def setPredictedValue(self, val):
        if not hasattr(self, 'info'):
            self.info = TlmyVarInfo()
            
            
        self.info.calSPredictedValue = str(val)
        
        #It doesn't overload the tlmyvar save method in order to 
        #improve massive tlmyvar save process
        self.info.save()
        
        return self.info.calSPredictedValue

    def __is_set(self, x, n):
      return x & 2**n != 0 
    
    
    @classmethod
    def create(cls, **kwargs):
      result = cls()
      if('telemetry_type' in kwargs):
        result.tlmyVarType = kwargs['telemetry_type']
      
      if('raw' in kwargs):
        
        tt = result.tlmyVarType
        rd = kwargs['raw']
        payload = rd.getPayloadBlob()
        
        if (tt.varSubType==1):
            #Telemetria derivada
            raw = rd.id
        else:            
            if tt.bitsLen >= 8:
                #Antiguamente se hacia la cuenta, ahora el dato se puede sacar se ctype,
                #pero cuidado que debe existir coherencia entre bitslen y ctype length, una buena
                #constraint para poner #bitLen_div =tt.bitsLen // 8
                raw = unpack(tt.ctype.format,  payload[tt.position:tt.position+tt.ctype.length])[0]
            elif tt.bitsLen == 1:
                raw = result.__is_set(payload[tt.position], tt.subPosition)
            else:
                #Not implemented yet
                pass           
        
        result.code           = tt.code
        result.tlmyRawData    = rd
        result.setValue(raw, rd.pktdatetime)
        
      elif('value' in kwargs and 'tstamp' in kwargs):
        value  = kwargs['value']
        tstamp = kwargs['tstamp']
        result.code           = result.tlmyVarType.code
        result.tlmyRawData    = None
        result.setValue(value, tstamp)
        
        
      else:
        raise Exception("args error")
      
      return result
        
    """
    def __init__(self, *args, **kwargs):
      super(TlmyVar, self).__init__(args, kwargs)
      if('raw' in kwargs and 'telemetry_type' in kwargs):
        self.tlmyVarType = kwargs['telemetry_type']
        tt = self.tlmyVarType
        rd = kwargs['raw']
        payload = rd.getPayloadBlob()
        
        if (tt.varSubType==1):
            #Telemetria derivada
            raw = rd.id
        else:            
            if tt.bitsLen >= 8:
                #Antiguamente se hacia la cuenta, ahora el dato se puede sacar se ctype,
                #pero cuidado que debe existir coherencia entre bitslen y ctype length, una buena
                #constraint para poner #bitLen_div =tt.bitsLen // 8
                raw = unpack(tt.ctype.format,  payload[tt.position:tt.position+tt.ctype.length])[0]
            elif tt.bitsLen == 1:
                raw = self.__is_set(payload[tt.position], tt.subPosition)
            else:
                #Not implemented yet
                pass
            
        
        self.code           = tt.code
   
        self.tlmyRawData    = rd
        self.setValue(raw, rd.pktdatetime)
        
        
        
      else:
        pass#raise Exception("args error")
    """  
    
    def setValue(self, raw, dt=datetime.now(utc)):
        self.rawValue = raw
        if self.tlmyVarType.ctype.varType==self.tlmyVarType.ctype.STRING:
            rawUnpacked = unpack('{}s'.format(len(raw)), raw)[0]
        else:
            rawUnpacked = unpack(self.tlmyVarType.ctype.format, raw)[0]
        #
        if self.tlmyVarType.calibrationMethod: 
            if not self.tlmyVarType.calibrationLogic:
                #Optimizacion, amplia mejora para evitar carga de bibliotecas innecearias, si la clase ya fue cargada no se vuelve a cargar
                klass = globals()[self.tlmyVarType.calibrationMethod.aClass]
                instance = klass()
                methodToCall = getattr(instance, self.tlmyVarType.calibrationMethod.aMethod)
                self.tlmyVarType.calibrationLogic = methodToCall
            else:
                #print("CALIBRACION PREVIAMENTE CARGADA")
                pass #Calibracion ya cargada   
            value = self.tlmyVarType.calibrationLogic(self.tlmyVarType,  rawUnpacked)
        else:
            value = rawUnpacked
       

        #Ya no pregunto por el tipo de interpretacion sino por el 
        #resultado(self.tlmyVarType.ctype.varType==self.tlmyVarType.ctype.INTEGER)
        if isinstance(value, float):        
            self.calFValue = value
            self.calSValue = '%.2f' % self.calFValue
        elif isinstance(value, int):
            self.calIValue = value
            self.calSValue = str(self.calIValue)
        elif isinstance(value, bool):
            self.calBValue = value
            self.calSValue = str(self.calBValue)
        elif isinstance(value, bytes):
            self.calSValue = value.decode('utf-8')
            
        if isinstance(value, int) or isinstance(value, float) :
            if (value>=self.tlmyVarType.limitMaxValue and value<=self.tlmyVarType.limitMinValue):
                raise Exception("Invalid value in var "+self.tlmyVarType.code)  

            #Check if outlier
            if self.tlmyVarType.checkoutlier:
                if value>self.tlmyVarType.outliermaxlimit or value<self.tlmyVarType.outlierminlimit:
                    self.outlier = True
            
        self.tstamp         = dt
        self.UnixTimeStamp  = dt.timestamp()*1000
         

        return self
    
    def __str__(self):
        return self.calSValue+"-"+str(self.tstamp)

    def toJson(self):
        return json.dumps({"value":self.calSValue, "datetime":str(self.tstamp), "fullname":self.getFullName()})
    

    def getFullName(self):
        return self.tlmyVarType.fullName


    
class TlmyVarInfo(models.Model):
    calSPredictedValue   = models.CharField('Valor predecido como string de la variable de telemetria', null=True, default=None, max_length=24, help_text='Valor predecido como string de la variable de telemetria')
    genTime              = models.FloatField('Time to calculate the value', default=0)
    
    tlmyVar = models.OneToOneField(
        TlmyVar,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='info'
    )

    
    
    