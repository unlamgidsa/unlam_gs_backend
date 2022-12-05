'''
Created on Sep 28, 2016

@author: ubuntumate
'''
import unittest

from GroundSegment.models.Satellite import Satellite
from GroundSegment.models import Tle, SatelliteState
from GroundSegment.models.Alarm.Criticity import Criticity
from django.utils.timezone import datetime, now, timedelta, utc
from _datetime import datetime
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Alarm.Alarm import Alarm
#from GroundSegment.models.Site import Site
from django.core.exceptions import ObjectDoesNotExist
from GroundSegment.models.Notification.Contact import Contact
from GroundSegment.models.Notification.MessageTemplate import MessageTemplate
from GroundSegment.models.Notification.NotificationType import NotificationType
from GroundSegment.models.Notification.AlarmTypeNotificationType import AlarmTypeNotificationType

class Test(unittest.TestCase):


    def testSendAlarmaNotification(self):
        try:        
        
            ss = SatelliteState.objects.get(code="NOMINAL")
        except ObjectDoesNotExist:
            ss = SatelliteState()
            ss.code = "NOMINAL"
            ss.description = "NOMINAL"
            ss.save()
        
        
        try:
            sat2 = Satellite.objects.get(code="FS2017")
        except ObjectDoesNotExist:
            sat2 = Satellite.new("FS2017", "FS2017", 25549, ss)
            sat2.save()
            
        cr = Criticity()
        cr.code = "ALTA"
        cr.color = 0
        cr.description = "ALTA"
        cr.save()
        
        
        at = AlarmType()
        at.code = "VA05"
        at.description = "Baja tension en panel A "
        at.criticity = cr
        at.procedure = "revisar x e y. Infomar del problema al responsable de potencia y apagar el dispositivo x"
        at.timeout = 60
        at.save()
        
        con = Contact()
        con.name = "Pablo Soligo"
        con.email = "pablito373@hotmail.com"
        con.save()
        
        mt = MessageTemplate()
        mt.name = "Test message template"
        mt.subject = "Mensaje de alerta"
        mt.text = "A sucedido la alarma con id <pk/> y su criticidad es <alarmType.criticity.description/> se recomienda <alarmType.procedure/>"
        mt.save()
        
        nt = NotificationType()
        nt.code = "EMAIL"
        nt.description = "EMAIL"
        nt.save()
        
        atnt = AlarmTypeNotificationType()
        atnt.notificationType = nt
        atnt.alarmType = at
        atnt.messageTemplate = mt
        atnt.save()
        atnt.contacts.add(con)
        atnt.save()
        
        

        from django.utils.timezone import datetime, now, timedelta, utc

        al = Alarm.new(sat2, at, datetime.now(utc))
        
        
        
        
        
        
        
            
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSendAlarmaNotification']
    unittest.main()