'''
Created on 27 jun. 2018

@author: pablo

from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyRawData import TlmyRawData
sat = Satellite.objects.get(code="LITUANICASAT2")
TlmyRawData.objects.filter(source="LITUANICASAT2").delete()
TlmyVar.objects.filter(tlmyVarType__satellite=lit).delete()

from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVar import TlmyRawData
TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").delete()
TlmyRawData.objects.filter(source="SACD").delete()
'''

import os, sys, time
from sys import argv

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from GroundSegment.models.Satellite import Satellite
   
from GroundSegment.celery import TaskSATNOGSAdapter
from Calibration.tasks import autodiscover

    

if __name__ == '__main__':
        
    
    print("Tarea testeada por consola")
    #tlmySatDecode("LITUANICASAT2")
    #FS2017DBAdapter()
    
    #issta = ISSTelemetryAdapter()
    
    while(True):    
        #sats = Satellite.objects.filter(active=True)
        #for sat in sats:
        #    sat.tmlyVarType.update(lastUpdate = None)
            #tlvs = sat.tmlyVarType.all();
            #for tvt in tlvs:
            #    tvt.lastUpdate = None
            #    tvt.save()
        #print("Procesando archivos SACD")
        #SACDFileAdapter()        
        #Autodiscover
        #print("Descubriendo nuevas funciones...")
        #autodiscover(None)
        TaskSATNOGSAdapter()
        print("fin ciclo...")
        time.sleep(60*60*12) #12 horas
        #time.sleep(5)
    print("fin proceso..")