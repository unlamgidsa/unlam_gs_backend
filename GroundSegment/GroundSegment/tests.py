'''
Created on 16 de ago. de 2016

@author: pabli

Deprecated!! meter los test dentro de Verification
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


#import django



class Test(unittest.TestCase):


    def setUp(self):
        pass
        
                

    def tearDown(self):
        pass
    
    @classmethod
    def setUpClass(cls):
        """
        Crea los maestros de operacion para el resto de los test de esta unidad
        """
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
            sat2 = Satellite.new("FS2017", "FS2017", 25546, ss)
  
            sat2.save()
            

        
    
    def testSetLastTle(self):
        self.setUpClass()
        sat = Satellite.objects.get(code="FS2017")
        
        import os
        settings_dir = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
        FILES_FOLDER = os.path.join(PROJECT_ROOT, 'Files/')
        
        

       
        path = FILES_FOLDER+'99937TLE.txt'
        
        sat.setLastTLE(path)
        
        ln1 = sat.getLastTLE().getLine1()
        ln2 = sat.getLastTLE().getLine2()
        
        print("Linea 1> ", ln1)
        print("Linea 2> ", ln2)
  
    def testNextPass(self):
        """
        Testeo no finalizado
        
        
        sat = Satellite.objects.get(noradId="25544")
        
        site = Site()
        site.setLatitude(-31.524075)
        site.setLongitude(-64.463522)
        site.setAltitude(730.0)
        site.save()
        
        fro = datetime.utcnow()
        to = datetime.utcnow() + timedelta(minutes=30)
        
         
        
        site.getPass(fro, to, sat)
        """   
#
#     def testNewAlarm(self):
#         
#         ss = SatelliteState()
#         ss.code = "NOMINAL"
#         ss.description = "NOMINAL"
#         ss.save()
#         
#         sat2 = Satellite.new("FS2017", "FS2017", 25544)
#         sat2.state = ss
#         sat2.save()
#         
#         cr = Criticity()
#         cr.code = "Grave"
#         cr.description = "Grave"
#         cr.color = "#00000"
#         cr.save()
#         
#         at = AlarmType()
#         at.code = "Panel no se que"
#         at.description = "Panel no se que"
#         at.criticity = cr
#         at.procedure = "PP"
#         at.timeout = 60
#         at.save()
#         
#         sat = Satellite.objects.get(noradId="25544")
#         import random
#         
#         pool= list( AlarmType.objects.all() )
#         random.shuffle( pool )
#         at = pool[0]
#         
#         al = sat.newAlarm(at)
#         
#         print(al.dtArrival)
#     
#     def testGetLastTle(self):
#         
#         
#         sat = Satellite.objects.get(noradId="1553")
#         lasttle = sat.getLastTLE()
# 
#         
#         #dt = datetime.now(utc)+timedelta(days=1)
#         
#         #dt fijo
#         
#         #2016-08-30 14:53:01.823895+00:00
#         dt = datetime(2016, 9, 30, 14, 53, 0)
#         
#         print(lasttle.lines)
#         
#         for i in range(10):
#             print("Celestial position 1: ", sat.getCelestialPosition(dt+timedelta(minutes=i)))
#         
#         
#         
#         sat.getPass(dt, dt+timedelta(days=1), None)
#          
#         
        
    """

    def testSatelliteCreationAndCount(self):
        #pass

        for i in range(0,9):
            code        = "Code"+str(i)
            description = "Description"+str(i)
            noradId     = i
            Satellite.new(code, description, noradId).save()
            
   

            
        
        sl = Satellite.objects.all()
        
        self.assertEqual(len(sl), 9, "La cantidad de satelites recuperados es distinta a la de satelites creados") 
            
    """        
        
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSatelliteCreationAndSearch']
    unittest.main()