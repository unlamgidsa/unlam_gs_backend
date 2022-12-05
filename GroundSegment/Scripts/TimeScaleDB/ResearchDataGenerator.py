'''
Created on 30 abr. 2020

@author: pablo
'''
#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/ResearchDataGenerator.py

import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj_path = '/home/pablo/git/GroundSegment/GroundSegment/'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from Simulators.DCSSimulator import satellite

from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from Telemetry.models.FrameType import FrameType
from Telemetry.models.TlmyVar import TlmyVar
import numpy as np
from datetime import datetime, timedelta
from random import randint
import time

if __name__ == '__main__':
    
    amounttvt = 7500
    #DBSat1, DBSat2, DBSat3,
    #Satellite.objects.get(code="BDSat1"), 
    sats =  [Satellite.objects.get(code="BDSat1"), Satellite.objects.get(code="BDSat2"),  Satellite.objects.get(code="BDSat3")]
    #sats =  [Satellite.objects.get(code="BDSat1")]
    
    subsystem = SubSystem.objects.get(code="ALL")
    ctypeShortBigEndian = CType.objects.get(code="short big-endian")
    umDiscrete = UnitOfMeasurement.objects.get(code="(D)")
    
    
    INTEGER = 0;
    FLOAT = 1;
    
    #linealCalibration = Calibration.objects.get(aClass="GCalibration", aMethod="linealCalibration");
   
    #Creo las 7500 tipo de variables de telemetria sino existen aun!
    
   
    
    ftid = 600
    for sat in sats:
        
        for tvt in sat.tmlyVarType.all():
            tvt.tlmyVars.all().delete()
            
        sat.tmlyVarType.all().delete()
        ft = FrameType.objects.filter(description="AllTelemetry", satellite=sat).first() # get_or_create(aid=ftid, , satellite=sat)
        
            
        ftid = ftid + 1;
        for i in range(0,amounttvt):
            
            tvt, created = TlmyVarType.objects.get_or_create(code=sat.code+"_AV"+i.__str__(), 
                                                     description=sat.code+"_AV"+i.__str__(),
                                                     satellite=sat,
                                                     varType=INTEGER,
                                                     position=i * 2,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=subsystem,
                                                     unitOfMeasurement=umDiscrete,
                                                     ctype=ctypeShortBigEndian,
                                                     frameType=ft)
        
   

    
    
    
        tvts = sat.tmlyVarType.all()
        
        #for tvt in tvts:
        #    tvt.tlmyVars.all().delete()
        
        tlvsl = []
        
        
        end     = datetime(2020,1,1,0,0,8);
        start   = datetime(2020,1,1,0,0,0);
        
        start   = start.astimezone();
        end     = end.astimezone()
        
        valant = start;
        while(start<end):
            
            for tvt in tvts:
                
                if randint(0, 4)==2:
                    fcv = int(round(np.sin(start.timestamp())*10));
                else:
                    fcv = int(round(np.sin(valant.timestamp())*10));
                
                #g_time = time.time()
                tvar                = TlmyVar()
                tvar.code           = tvt.code
                tvar.tlmyVarType    = tvt
                #tvar.satellite      = tvt.satellite
                tvar.tlmyRawData    = None
                #raw+datetime
                #l_time = time.time()
                tvar.setValue(fcv, start) 
                #l_ftime =  time.time()
                tlvsl.append(tvar)
                #g_ftime = time.time();
                #print("totals:", g_ftime-g_time, l_ftime-l_time,  ((l_ftime-l_time)/(g_ftime-g_time))*100)
                
                
            print("Salvando...", start);
            TlmyVar.objects.bulk_create(tlvsl)   
            #Salvar en hipertabla
            TlmyVar._meta.db_table = "Telemetry_htlmyvar"
            TlmyVar.objects.bulk_create(tlvsl)   
            
            TlmyVar._meta.db_table = "Telemetry_tlmyvar"
            print("Salvado->", start);
            tlvsl.clear()
            valant = start
            start  = start + timedelta(seconds=8)
        
    print("Fin de programa")
     
        