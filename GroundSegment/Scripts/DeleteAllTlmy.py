'''
Created on 9 may. 2019

@author: psoligo
'''

import os, sys, time

from datetime import datetime
from django.db.models import Q


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()


from GroundSegment.models.Satellite import Satellite
#from Telemetry.models.BLTlmyVar import BLTlmyVar
from CODS.models import Ephemeride
from Telemetry.models.TlmyRawData import TlmyRawData
from types import FrameType
if __name__ == '__main__':
    sats = Satellite.objects.filter(~Q(code="FS2017"))
    
    
    Ephemeride.objects.all().delete()
    for sat in sats:
        deleteBlockSize = 5000
        #TlmyVar.objects.filter(tlmyVarType__satellite=sat).delete()
        
        print("Eliminados raws de ", sat.code)
        for tvt in sat.tmlyVarType.all():
            tvt.tlmyVars.all().delete()
            print("Borrado tipo ", tvt.code)  
        
        rds = sat.rawdatas.all()[:100] 
        while(rds.count()>0):
            for rd in rds:
                rd.delete()
            print("Borrando raw ")
                
            rds = sat.rawdatas.all()[:100] 
        
        
            
        
    print("Proceso de borrado finalizado")