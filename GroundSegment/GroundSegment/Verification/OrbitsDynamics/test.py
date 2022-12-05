'''
Created on Apr 14, 2017

@author: ubuntumate
'''

import unittest
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from datetime import datetime, timedelta
from GroundSegment.models.Eclipse import Eclipse
from django.utils.timezone import pytz


class Test(unittest.TestCase):


    def test01DownloadLastTle(self):
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="SACD", description="SACD", noradId=37673, state=ss)

        if created:
            pass
        
        self.assertEqual(Satellite.objects.count(), 1, "Error en la cantidad de satelites")
            
    def test02NewFutureTLE(self):
        """
        Como es una consulta sobre un TLE con fecha futura el objecto debe retornar el mejor TLE posible
        y ese se corresponde con la fecha del dia actual... 
        """
        ss, created  = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
        
        tle = sat.getTLE(datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(days=5))
        
        self.assertEqual(tle.epoch.date(), datetime.utcnow().date(), "La fecha del mejor TLE para un analisis futuro no coincide con el dia de hoy")
        
    def test03NewPastTLE(self):
        """
        Como se solicita una fecha en el pasado y el TLE no ha sido descargado aun debe descargarlo
        y persistirlo. La epoca del TLE debe coincidir con el rango pasado como parametro
        """
        ss, created  = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
        
        afrom   = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=7)
        ato     = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=5)
        
        tle = sat.getTLE(afrom, ato)
        
        
        self.assertTrue(afrom.date() <= tle.epoch.date() <= ato.date())
        
        
        
    def test04DownloadedTLE(self):
        """
        En este test se solicita un tle al satelite con fecha pasada. Inmediatamente despues se vuelve a solicitar un tle pasando
        las mismas fechas y por tanto no se debe descargar de internet y se debe utilizar el previamente descargado.
        Se verifica que ambos objetos tengan la misma primary key para asegurarse de que son el mismo  y no se descargo un nuevo tle
        """
        ss, created  = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
        
        afrom   = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=7)
        ato     = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=5)
        
        tle = sat.getTLE(afrom, ato)
        
        
        tleDownload = sat.getTLE(afrom, ato)
        
        self.assertEqual(tle.pk, tleDownload.pk, "Se descargo un archivo TLE cuando ya existia uno.")
        
    def __test05TestEclipseEquality(self):
        
        ss, created  = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
        
        
        e1 = Eclipse()
        e1.startTime = datetime.utcnow().replace(tzinfo=pytz.UTC)
        e1.stopTime = e1.startTime+timedelta(minutes=60)
        e1.satellite = sat
        
        #Esto se harcodea hasta tener resuelto el methodo de satelite
        e1.tle = sat.getTLE(e1.startTime, e1.stopTime)
        e1.save()
        
        e2 = Eclipse()
        e2.startTime = (datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(seconds=15))
        e2.stopTime = e2.startTime+timedelta(minutes=60)
        e2.satellite = sat
        
        #Esto se harcodea hasta tener resuelto el methodo de satelite
        e2.tle = sat.getTLE(e1.startTime, e1.stopTime)
        e2.save()
        
        #e1==e2        
        self.assertEqual(e1, e2, "Dos eclipse que pertenecian al mismo satelite y eran cercanos en ventana de tiempo fueron considerados distintos")
        
    
    def test06TestTleDistance(self):
        
        ss, created  = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
        
        
        afrom   = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=1)
        ato     = datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(days=1)
        eps1 = sat.getEclipses(afrom, ato)
        
        
        afrom   = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=0)
        ato     = datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(days=1)
        eps2 = sat.getEclipses(afrom, ato)
        
        
        afrom   = datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(days=1)
        ato     = datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(days=1)
        eps3 = sat.getEclipses(afrom, ato)
        
        
        for e in eps3:
            print(e.startTime, e.stopTime, e.tleDistance, e.getDurationStr(), e.obsolete)
        
        print("------------------------------------------------------------")
        
        eps = Eclipse.objects.all().order_by('startTime')
        for e in eps:
            print(e.startTime, e.stopTime, e.tleDistance, e.duration, e.obsolete)
            
            
        
        
        
        
        
    """       
    
    def __test02abc(self):
        #Propagaciones en Lat y Long.
        #http://stackoverflow.com/questions/15937413/python-satellite-tracking-with-spg4-pyephem-positions-not-matching
        
        sat = Satellite.objects.get(code="SACD")       
        tle = sat.getLastTLE()
        print (tle.getLine1())
        print (tle.getLine2())
        eb = tle.getAsEphemBody()
        d = ephem.Date('2017/4/14 12:00')
    
        for k in range(10):
            eb.compute(d)
            print (d,eb.sublat,eb.sublong)
            d=ephem.date(d + ephem.minute)

#         

#         print (date,eb.sublat, eb.sublong)
        
    """    
        
        
        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test01DownloadLastTle']
    unittest.main()