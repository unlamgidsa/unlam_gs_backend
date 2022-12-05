'''
Created on Mar 26, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Command.Command import Command
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.models.Command.CommandTypeParameter import CommandTypeParameter
from GroundSegment.models.Command.
import PassScript
from GroundSegment.Managers.CommandManager import CommandManager

from django.utils.timezone import datetime, now, timedelta
import time

from django.core.exceptions import ObjectDoesNotExist
import pytz
from _datetime import tzinfo
import random

class Test(unittest.TestCase):


    def setUp(self):
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        
        try:
            sat = Satellite.objects.get(code="FS2017")
            
        except ObjectDoesNotExist:
            sat = Satellite.new("FS2017", "FS2017", 2017, ss)
            sat.save()
        
        self.sat = sat
        
        try:
            ct = CommandType.objects.get(code="GT")
            
        except ObjectDoesNotExist:
            ct = CommandType.create("GT", "Get Telemetry", sat, ss, False, 60, "Sin notas", 3, )
            ct.save()
            
        self.ct = ct
        
        self.cmdmgr = CommandManager(self.sat)

        
        

    def tearDown(self):
        pass



        
    def test01ManagerCreateCommand(self):
        
        
        sat = Satellite.objects.get(code="FS2017")
        cmdmgr = CommandManager(sat)
        pcms = cmdmgr.getPendingCommands()
        
        ct  = CommandType.objects.get(code="GT")
        
        
        
        cmd = cmdmgr.newCommand(ct, (datetime.utcnow()+timedelta(minutes=60)).replace(tzinfo=pytz.UTC) )
        
        
        
    def test02ManagerPendingCommands(self):
        
        sat = Satellite.objects.get(code="FS2017")
        ct  = CommandType.objects.get(code="GT")
        
        cmdmgr = CommandManager(sat)
        cmdmgr.expirateAll()
        
        adt = (datetime.utcnow()+timedelta(seconds=2)).replace(tzinfo=pytz.UTC)
        cmd1 = cmdmgr.newCommand(ct, adt)
        cmd1.send()
        cmd2 = cmdmgr.newCommand(ct, adt)
        cmd2.send()
        
        self.assertEqual(cmdmgr.getPendingCommands().count(), 2, "La cantidad de comandos pendientes no es la correcta")
        
        cmdmgr.expirateAll()
    
    def test03SendCommands(self):
        
        sat = Satellite.objects.get(code="FS2017")
        ct  = CommandType.objects.get(code="GT")
        
        cmdmgr = CommandManager(sat)
        cmdmgr.expirateAll()
        
        adt = (datetime.utcnow()+timedelta(seconds=120)).replace(tzinfo=pytz.UTC)
        cmd1 = cmdmgr.newCommand(ct, adt)
        cmd1.send()
        cmd2 = cmdmgr.newCommand(ct, adt)
        cmd2.send()
        
        pcommands = cmdmgr.getPendingCommands()
        for c in pcommands:
            if random.randint(1, 5)==3:
                c.setFailed()
            else:
                c.setExecuted()
        
        self.assertEqual(cmdmgr.getPendingCommands().count(), 0, "La cantidad de comandos pendientes no es la correcta")
        
    
    def test04CommandStates(self):
        
        self.cmdmgr.expirateAll()
        
        adt = (datetime.utcnow()+timedelta(seconds=120)).replace(tzinfo=pytz.UTC)
        cmd = self.cmdmgr.newCommand(self.ct, adt, adt)
        cmd.send()
        
        self.assertEqual(cmd.getState()[1], cmd.COMMAND_STATE[0][1] , "El estado del commando no es el correcto para un comando recien creado")
        
        cmd.setExpirated()
        
        self.assertEqual(cmd.getState()[1], cmd.COMMAND_STATE[4][1] , "El estado del commando no es el correcto para un comando recien creado")
        
    def test05InContact(self):
        
        self.assertFalse(self.sat.inContact, "Error al obtener situacion de enlace del satelite")
        
        self.sat.setInContact(True)
        
        self.assertTrue(self.sat.inContact, "Error al obtener situacion de enlace del satelite")
        
        self.sat.setInContact(False)
        
        self.assertFalse(self.sat.inContact, "Error al obtener situacion de enlace del satelite")
        
        
        
    
    def test99ManagerFlushPendingCommand(self):
        
        sat = Satellite.objects.get(code="FS2017")
        ct  = CommandType.objects.get(code="GT")
        
        cmdmgr = CommandManager(sat)
        cmdmgr.expirateAll()
        
        adt = (datetime.utcnow()+timedelta(seconds=2)).replace(tzinfo=pytz.UTC)
        cmd1 = cmdmgr.newCommand(ct, adt)
        cmd1.send()
        cmd2 = cmdmgr.newCommand(ct, adt)
        cmd2.send()
        
    
        """
        Espero 3 segundos a que esten vencidos
        """
        time.sleep(3)
        """
        Se fuerza a que pasen los segundos y los comandos deberian estar vencidos
        """
        self.assertEqual(cmdmgr.getPendingCommands().count(), 0, "La cantidad de comandos pendientes no es la correcta")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCommand']
    unittest.main()