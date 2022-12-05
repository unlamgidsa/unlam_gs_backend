'''
Created on Mar 11, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Tle import Tle
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Sitio import Sitio
from django.utils import timezone
from datetime import timedelta
from _datetime import tzinfo
from django.utils.timezone import pytz
from GroundSegment.models.Country import Country
from GroundSegment.models.State import State

import os, sys




class testTle(unittest.TestCase):

    def setUp(self):
        print("SETUP-----------------------------")

    
    def test01Descarga(self):
        try:
            
            ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
            
            
            iss = Satellite.new("ISS", "Estacion espacial internacional", 25544, ss)
            iss.save()
            tle = iss.getLastTLE()
            
            epoch = tle.getEpoch()
            
            """
            La epoca del tle debe estar entre ayer y mañana
            """
            yesterday = (timezone.datetime.utcnow()-timedelta(days=1) ).replace(tzinfo=pytz.utc)
            tomorrow = (timezone.datetime.utcnow()+timedelta(days=1) ).replace(tzinfo=pytz.utc)
            
            self.assertTrue( ( epoch>=yesterday  ) and \
                             ( epoch<=tomorrow  ), \
                             "Last tle datetime is incorrect" \
                            )\
                              
            
            newtle = iss.getLastTLE()
            
            
            
            self.assertTrue(tle.getEpoch()==newtle.getEpoch(), "Two downloaded TLE at the same time")
            
            """
            Ahora el tle esta actualizado, no debe descargar nuevamente
            """
            
        
        except Exception as ex:
            self.fail("Error durante el test de descarga: "+str(ex))
            
            
    def test02EphemBody(self):
        
        
        iss = Satellite.objects.get(code="ISS")
        tle = iss.getLastTLE()
        eb = tle.getAsEphemBody()
        self.assertIsNotNone(eb, "No es generado el objeto tle como body")
        
    def test03PassGeneration(self):
        
        """
        proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DtnSatSimulator.settings")
        sys.path.append(proj_path)
        os.chdir(proj_path)
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        """
        
        
        
        country = Country.objects.get_or_create(code="ARG", name="Argentina", description="Argentina")
        state   = State.objects.get_or_create(code="COR", name="Cordoba", description="Cordoba", country=country[0])
        st      = Sitio.objects.get_or_create(name="ETC", lat=-31.5240, lon=-64.4635, h=730, maskElev=0.0, state=state[0])
        
        
        iss = Satellite.objects.get(code="ISS")
        tle = iss.getLastTLE()
        eb = tle.getAsEphemBody()
        
        afrom = timezone.now()
        ato = afrom+timedelta(days=3)
        
        st[0].getPasses(iss, afrom, ato)
        
        
            
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDescarga']
    unittest.main()