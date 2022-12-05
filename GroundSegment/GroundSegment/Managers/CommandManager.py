'''
Created on Mar 27, 2017

@author: ubuntumate
'''

"""
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.Managers.CommandManager import CommandManager
from GroundSegment.models.Satellite import Satellite
from django.utils.timezone import datetime, now, timedelta


sat = Satellite.objects.get(code="FS2017")
ct = CommandType.objects.get(code="GT")

mgr = CommandManager(sat)
mgr.newCommand(ct, datetime.now()+timedelta(minutes=5))
cmd.send()
pc = mgr.getPendingCommands()


c = pc[0]
c.getState()
"""


from ..models.Command.Command import Command
from ..models.Command.CommandType import CommandType
from ..models.Satellite import Satellite

from django.db.models import Q
from django.utils.timezone import datetime, now, timedelta
import pytz
from django.db import models

class CommandManager(models.Manager):
    '''
    classdocs
    Administra la creacion de comandos, quiza sea mejor hacerlos desde el satellite directamente
    
    '''
    


    def __init__(self, satellite):
        '''
        Constructor
        '''
        self.satellite = satellite
        
        
    def expirateAll(self):
        pc = self.getPendingCommands()
        for c in pc:
            c.setExpirated()
        
        return pc.count()
        
    def newCommand(self, commandType, expiration, timetag=datetime.utcnow().replace(tzinfo=pytz.UTC) ):
       
        cmd = Command()
        
        if commandType.satellite!=self.satellite:
            raise Exception("Este tipo de comando no puede ser aplicado al satelite pasado como parametro")
        
        cmd.satellite    = self.satellite
        cmd.commandType  = commandType
        cmd.created      = now()
        cmd.sent         = None
        cmd.retry        = 0
        cmd.expiration   = expiration
        cmd.executeAt    = timetag.replace(tzinfo=pytz.UTC) 
        #Mejorar la forma en que se trabajan las enumeraciones!
        cmd.state        = 0
        
        return cmd
    
    
    def getCommandTypes(self):
        return CommandType.objects.all()
    
    
    def __setExpiredCommands(self):
        cmds = Command.objects.filter(Q(satellite=self.satellite)&
                                      Q(expiration__lte= datetime.utcnow().replace(tzinfo=pytz.UTC))&
                                      Q(state__in=[0,]))
       
        
        
        for c in cmds:
            c.setExpirated()
        
        return cmds.count()
    
    def getPendingCommands(self):
        """
        Mato los comandos vencidos
        """
        self.__setExpiredCommands()
        
        ids = []
        cmds = Command.objects.filter(Q(satellite=self.satellite)&Q(state=0)).order_by('pk')
        for cmd in cmds:
            if cmd.parameters.count()==cmd.commandType.parameters.count():
                ids.append(cmd.pk) 
        
        
        return Command.objects.filter(pk__in=ids).order_by('executeAt')
        