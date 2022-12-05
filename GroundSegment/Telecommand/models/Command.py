'''
Created on Mar 24, 2017

@author: ubuntumate
'''
from django.db import models
from .CommandType import CommandType
from GroundSegment.models.Satellite import Satellite

from django.utils.timezone import datetime, now, timedelta
import pytz
from datetime import timezone
from _ast import Try
from binascii import hexlify
from django.db.models.deletion import PROTECT

#from GroundSegment.models.Satellite import Satellite
#from GroundSegment.models.SatelliteState import SatelliteState

class Command(models.Model):
    
    
    COMMAND_STATE = (
        (0, 'Pending'),
        (1, 'Sent'),
        (2, 'Failed'),
        (3, 'Executed'),
        (4, 'Expirated'),
    )


    
    
    commandType = models.ForeignKey(CommandType, related_name="commands", on_delete=PROTECT)
    created     = models.DateTimeField()
    
    #Tiempo en el cual debe ser ejecutado
    executeAt   = models.DateTimeField(default=datetime(2000, 1, 1, tzinfo=timezone.utc))
    
    sent        = models.DateTimeField(null=True)
    executed    = models.DateTimeField(null=True)
    state       = models.IntegerField(choices=COMMAND_STATE, default=0)
    retry       = models.IntegerField(default=0)
    """
    TODO: Meter los parametros del comando!!!
    """
    satellite   = models.ForeignKey(Satellite, related_name="commands", on_delete=PROTECT)
    
    
    #Tiempo hasta el cual se puede intentar enviar    
    expiration  = models.DateTimeField(default=datetime(2000, 1, 1, tzinfo=timezone.utc))
    
    #TODO, quitar null=True
    binarycmd   = models.BinaryField("Comando en formato binario listo para ser enviado por TCP/IP", null=True)
    
    
    def getBinaryCommand(self):
        result = bytearray()
        dl = self.getBinaryCommandLen()
        for i in range(dl):
            result += self.binarycmd[i]
                
        return result
    
    def getBinaryCommandLen(self):
        return len(self.binarycmd)
    
    def setExpirated(self):
        self.state  = 4
        self.save()
    
    def setSent(self):
        if self.retry>=self.commandType.maxRetry:
            self.setFailed()
        else:
            if self.sent==None:
                self.sent   = datetime.utcnow().replace(tzinfo=pytz.UTC)
            self.state  = 1
            self.retry = self.retry + 1
            self.save()
            
    def setExecuted(self):
        self.executed = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.state = 3
        self.save()
        
    def setFailed(self):
        self.executed = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.state = 2
        self.save()
        
    
    
    def send(self):
        self.save()
        
    def getState(self):
        return self.COMMAND_STATE[self.state]
    
    def getTypeCommand(self):
       
        if self.commandType.parameters.count()==0:
            return 0
                    
        listParameterCommand = self.commandType.parameters.all().values_list('code', flat=True)
    
        return listParameterCommand

    def addParameters(self,*args):
        """Los parametros se guardan en el orden que son ingresados
        """
    
        from GroundSegment.models.Command.CommandParameter import CommandParameter
        self.save()
        try:
            if (len(args))==(len(self.getTypeCommand())):
                    for value in args:
                        p = CommandParameter()
                        p.value = str(value)
                        
                        p.command = self
                        p.save()
            else:
                print("error")
        except:
            #Bug! Cambiar por un raise exception
            #print("Este comando no tiene parametros")                    
            raise Exception("The command hasn't parameters")
    
    def __str__(self):
        return "Cmd: "+str(self.pk)+" tipo: "+self.commandType.code

"""
Console test...
"""
    