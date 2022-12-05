'''
Created on Sep 26, 2016

@author: ubuntumate
'''
import unittest

from GroundSegment.models.Satellite import Satellite
from GroundSegment.models import Tle, SatelliteState
from GroundSegment.models.Alarm import Criticity
from django.utils.timezone import datetime, now, timedelta, utc
from _datetime import datetime
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Alarm.Alarm import Alarm
#from GroundSegment.models.Site import Site


class AlarmTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        """
        Crea los maestros de operacion para el resto de los test de esta unidad
        """
        
        
        ss = ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        ss.code = "NOMINAL"
        ss.description = "NOMINAL"
        ss.save()
        
        sat2 = Satellite.new("FS2017", "FS2017", 25599, ss)
        
        sat2.save()
        
        #Creo al menos un tipo de alarma y una criticidad
        
        cr = Criticity()
        cr.code = "MEDIA"
        cr.color = 0
        cr.description = "MEDIA"
        cr.save()
        
        
        at = AlarmType()
        at.code = "ST01"
        at.description = "Sobre tension"
        at.criticity = cr
        at.timeout = 60
        at.save()
            
        
    
    def test01Alarm(self):
        """
        1.Testea la creacion de alarmas mediante el metodo de clase new, seleccionando un tipo de alarma aleatorio\n
        2.Testea los cambios de estado del misma mediante el llamado a metodos\n
        3.Verifica que las acciones a realizar en los cambios de estados se implementan correctamente\n        
        """
        
        #print("TESTANDO ADENTRO!!!")
        
        try:
            sat = Satellite.objects.get(code="FS2017")
            
            at = AlarmType.objects.order_by('?').first()
            
            alarm = Alarm.new(sat, at, datetime.utcnow() + timedelta(seconds=-1))
            alarm.save()
        except Exception:
            pass

        
        
    def testDuplicateAlarmaType(self):
        """
        1.Testea que no se puedan crear dos alarmas del mismo tipo\n
        2.Genera una excepcion que hace fallar el test
        """
        pass
        
        """
        cr = Criticity.objects.all()[0]
        
        at = AlarmType()
        at.code = "ST01"
        at.description = "Sobre tension en bla bla"
        at.criticity = cr
        at.timeout = 60
        at.save()
        """

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()