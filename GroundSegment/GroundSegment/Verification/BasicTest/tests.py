'''
Created on Aug 14, 2017

@author: ubuntumate
'''
import unittest

# import sys 
# print('%s %s' % (sys.executable or sys.platform, sys.version))
# import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; import django
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()


# sys.path.insert(0, '../../models/')
# from SatelliteState import SatelliteState
# from Country import Country
# from Satellite import Satellite
# import TlmyVarType


from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Country import Country
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models import TlmyVarType


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test01SatelliteState(self):
        print("test.....")
        st1 = SatelliteState()
        st1.code = "Nominal"
        st1.description = "Nominal"
        st1.save()
        
        st2 = SatelliteState()
        st2.code = "Emergencia"
        st2.description = "Emergencia"
        st2.save()
        
        self.assertEqual(SatelliteState.objects.count(), 2, "La cantidad de estados es incorrecta")
        
        self.assertEqual(SatelliteState.objects.filter(code="Nominal").count(), 1, "No se encontro el estado!")
        
        
        
        
    def test02Country(self):
        country_1 = Country()
        country_1.code = "001"
        country_1.name = "Argentina"
        country_1.description = "Republica Argentina"
        country_1.save()
        

        country_2 = Country()
        country_2.code = "002"
        country_2.name = "Japon"
        country_2.description = "Japon"
        country_2.save()


        country_3 = Country()
        country_3.code = "003"
        country_3.name = "China"
        country_3.description = "Muralla China"
        country_3.save()


        self.assertEqual(Country.objects.count(), 3, "La cantidad de paises es incorrecta")
        
        self.assertEqual(Country.objects.filter(name="China").count(), 1, "No se encontro el pais!")
        
        self.assertEqual(Country.objects.first().name, "Argentina", "No se encontro el pais!")

    def test03Satellite(self):
        
        try:
            st = SatelliteState.objects.first()
            sat = Satellite.new("FS2017", "Satelite de formacion 2017", 98745, st)
            sat.save()
        except:
            pass
        
    def test04SatellitePendingCommands(self):
        
        sat = Satellite.objects.get(code="FS2017")

        cmd = sat.getPendingCommands()

        self.assertEqual(cmd.count(), 0, "Cantidad de comandos pendientes distinto a 0.")



        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()