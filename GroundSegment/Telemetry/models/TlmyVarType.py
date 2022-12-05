'''
Created on 3 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models
import sys

from GroundSegment.models.Alarm.Alarm import Alarm
from .Calibration import Calibration

from django.utils.timezone import datetime, now, timedelta, utc

from django.db.models.deletion import CASCADE, PROTECT

from .FrameType import FrameType
from .UnitOfMeasurement import UnitOfMeasurement
from unittest.util import _MAX_LENGTH
from GroundSegment.models.SubSystem import SubSystem
from GroundSegment.models.ModelDiffMixin import ModelDiffMixin
from django.db import transaction
from django.db import connection


class CType(models.Model):
    OTHER = -1
    INTEGER = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3

    VARTYPE = (
        (OTHER, 'other'),
        (INTEGER, 'integer'),
        (FLOAT, 'float'),
        (STRING, 'string'),
        (BOOLEAN, 'boolean'),
    )


    code                = models.CharField('Codigo del Tipo C', max_length=48, help_text='Codigo del Tipo C', unique=True, default="no det")
    format              = models.CharField('Codigo de desempaquetado asociado', max_length=6, default="no det")
    length              = models.IntegerField('Size of the CType', default=1)
    varType             = models.IntegerField("Tipo de dato, -1=Otro 0=Integer, 1=Float, 2=String", default=0, choices=VARTYPE) 
    tag                 = models.CharField('Free field for differents purpouses', null=True, max_length=64, help_text='Free Field')
    
    #groupDescription    = models.CharField()


    def __str__(self):
        return self.code
   
    @classmethod
    def createBasics(cls):
        ctypes = [
            ("c", "char", 0, 1),
            ("b", "signed char", 0, 1),
            ("B", "unsigned char", 0, 1),
            ("?", "bool",  0, 1),
            ("h", "short", 0, 2),
            ("H", "unsigned short", 0, 2),
            ("i", "int", 0, 4),
            ("I", "unsigned int", 0, 4),
            ("l", "long", 0, 4),
            ("L", "unsigned long", 0, 4),
            ("L", "long long", 0, 8),
            ("L", "unsigned long long", 0, 8),
            ("f", "float", 1, 4),
            ("d", "double", 1, 8),
            ("s", "string", 2, -1),
            ("z", "custom", 1, -1)
        ]

        endings = [
            ("<", "little-endian"),
            (">", "big-endian")
        ]       

        for ct in ctypes:
            for e in endings:
                #Si se encuentra el codigo de desempaquetado
                #se actualiza lo otro para que quede normalizado
                try:
                    o = cls.objects.get(format=e[0]+ct[0])
                    
                except cls.DoesNotExist as ex:
                    o = cls()
                    o.format = e[0]+ct[0]

                o.code          = ct[1]+" "+e[1]
                o.length        = ct[3]
                o.varType       = ct[2]
                o.save()


"""
#obsoleto, los tipos no se actualizan, telemetria
#en tiempo real via websockets
class TlmyVarTypeManager(models.Manager):
    

    def updateTlmyType(self, objs, fields):
        
        with transaction.atomic():
            with connection.cursor() as cursor:
                tids = ""
                for o in objs:
                    tfields = ""
                    argslist = []
                    for f in fields:
                        argslist.append(getattr(o, f))
                        tfields += "\""+f+"\""+"=%s,"
                    tfields = tfields[0:-1]
                
                    argslist.append(getattr(o, "id"))

                    sql = '''update public."Telemetry_tlmyvartype" set '''+tfields+''' where \"id\"=%s'''
                    ret = cursor.execute(sql, argslist)
                    
                    #ret = self.raw(sql, argslist)
                    #print("registros actualizados", ret)
    
"""

class TlmyVarType(models.Model):
   
    DIRECT = 0
    DERIVED = 1
    #objects     = TlmyVarTypeManager() 
    
    VARSUBTYPE = (
        (DIRECT, 'Direct'),
        (DERIVED, 'Derived'),
        
    )
    # , db_index=True
    code = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True, db_index=False)
    description = models.CharField('Decripcion del tipo de variable', max_length=100, help_text='Decripcion del satelite')
    
    satellite = models.ForeignKey('GroundSegment.Satellite', related_name="tmlyVarType", db_index=False, on_delete=CASCADE)
    
    limitMaxValue = models.FloatField("Maximo", default=99999.9)
    limitMinValue = models.FloatField("Minimo", default=-99999.9)
    
    maxValue = models.FloatField("Maximo valor tolerable", null=True, blank=True)
    minValue = models.FloatField("Minimo valor tolerable", null=True, blank=True)  # sys.float_info.min
    
    """
    lastRawValue = models.BigIntegerField(default=0)
    lastCalIValue = models.BigIntegerField(default=0)
    lastCalFValue = models.FloatField(default=0.0)
    lastCalBValue = models.BooleanField(default=False)
    lastCalSValue = models.CharField('Valor como string de la variable de telemetria', default="No defined", max_length=128, help_text='Valor como string de la variable de telemetria', null=True)
    lastUpdate = models.DateTimeField('Indica cuando se escribio la variable', null=True)  #
    tstamp = models.DateTimeField('Indica la fecha hora del dato suministrada por el equipo', default=datetime.strptime("1976-10-30 12:00:00 +0000", '%Y-%m-%d %H:%M:%S %z'))     
    """
       
    varSubType = models.IntegerField("Indica si es directa o derivada 0=Directa, 1=Derivada", default=0, choices=VARSUBTYPE)
    ctype = models.ForeignKey(CType, on_delete=PROTECT, related_name="tlmyVarTypes", default=1)
    
    alarmType = models.ForeignKey(Alarm, related_name="tmlyVarType", blank=True, null=True, db_index=False, on_delete=PROTECT) 
    calibrationMethod = models.ForeignKey(Calibration, related_name="tlmyVarTypes", blank=True, null=True, db_index=False, on_delete=PROTECT)
    calibrationLogic = None
    position = models.IntegerField(default=0)
    subPosition = models.IntegerField(default=0)
    bitsLen = models.IntegerField(default=0)
    
    frameType = models.ForeignKey(FrameType, related_name="tlmyVarTypes", null=True, on_delete=PROTECT)
        
    unitOfMeasurement = models.ForeignKey(UnitOfMeasurement, related_name="tlmyVarTypes", null=True, on_delete=PROTECT)
    
    subsystem       = models.ForeignKey(SubSystem, on_delete=PROTECT, related_name="tlmyVarTypes", null=True);
    tag             = models.CharField('Free field for differents purpouses', null=True, max_length=64, help_text='Free Field')
    checkoutlier    = models.BooleanField("Check if outlier", null=False, default=False)
    outliermaxlimit = models.BigIntegerField("Max outlier value", null=False, default=0);
    outlierminlimit = models.BigIntegerField("Min outlier value", null=False, default=0);
    
    @property
    def fullName(self):
        #return self.satellite.code+"."+self.code
        return ''.join(
            [self.satellite.code,'.',self.code])

    def __str__(self):
        return self.code + ", sat: " + self.satellite.code
    
    def getTimeFromLastUpdate(self):
        pass

    
    def getValue(self):
        # Retorna el valor en funcion del tipo
        if self.ctype.varType == self.ctype.INTEGER:
            return self.lastCalIValue
        elif self.ctype.varType == self.ctype.FLOAT:
            return self.lastCalFValue
        elif self.ctype.varType == self.ctype.BOOLEAN:
            return self.lastCalBValue
        else:
            return self.lastCalSValue
        
    def setValue(self, value, dt=datetime.now(utc)):
        fieldstosave = []
        #ir modificando esto por ctype, dejar obsoleto el varType
        # si el valor cambio actualizo
        if self.ctype.varType == self.ctype.INTEGER:
            self.lastCalIValue = value
            fieldstosave.append('lastCalIValue')
        elif self.ctype.varType == self.ctype.FLOAT:
            self.lastCalFValue = value
            fieldstosave.append('lastCalFValue')
        elif self.ctype.varType == self.ctype.BOOLEAN:
            self.lastCalBValue = value
            fieldstosave.append('lastCalBValue')
        else:
            self.lastCalSValue = value
            fieldstosave.append('lastCalSValue')
        # django.utils.timezone.
        self.lastUpdate = datetime.now(utc)
        fieldstosave.append('lastUpdate')
        
        if self.ctype.varType == self.ctype.FLOAT:
            self.lastCalSValue = '%.2f' % self.getValue()
        else:
            self.lastCalSValue = str(self.getValue())
        
        self.tstamp = dt
        fieldstosave.append('tstamp')
        # Solo salvar lo que debo salvar, no mas....
        #self.save(update_fields=fieldstosave)
        return fieldstosave

    def getFullName(self):
        #TODO: Persist this proporty in database for performance reason
        return self.fullName
        
    