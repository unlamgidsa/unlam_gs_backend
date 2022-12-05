'''
Created on 29 mar. 2019

@author: psoligo
'''

import os, sys, time
from types import FrameType
from datetime import datetime

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.FrameType import FrameType
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from Telemetry.models.TlmyVarType import CType
from Telemetry.models.Calibration import Calibration
from Telemetry.models.Coefficient import Coefficient

if __name__ == '__main__':
    sat = Satellite.objects.get(code="SACD")
    deleteBlockSize = 5000
    #TlmyVar.objects.filter(tlmyVarType__satellite=sat).delete()
    TlmyRawData.objects.filter(source="SACD").delete()
    tlmt = TlmyVarType.objects.filter(satellite__code="SACD")
    tlmids=TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").values_list('id', flat=True)[0:deleteBlockSize]
    
    
    ltypeFloat = TlmyVarType.FLOAT
    ltypeInteger = TlmyVarType.INTEGER
    ltypeboolean = TlmyVarType.BOOLEAN
    
    
    ft = FrameType.objects.get(description="AllTelemetry")
    ss = SubSystem.objects.get(code="ALL")
    um = UnitOfMeasurement.objects.get(code="(D)")
    ct = CType.objects.get(code="signed char")
    linealCalibration = Calibration.objects.get(aClass="GCalibration", aMethod="linealCalibration");
    
    
    while(len(tlmids)>0):
        dts = datetime.utcnow()
        TlmyVar.objects.filter(pk__in=tlmids).delete()
        tlmids=TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").values_list('id', flat=True)[0:deleteBlockSize]
        print("Bloque de, ", deleteBlockSize, "  borrado en ", (datetime.utcnow()-dts).total_seconds())
        
    
        
    tttd = sat.tmlyVarType.filter(code__contains="AV")
    for tt in tttd:
        tt.coefficients.all().delete()
        tt.delete()   
    
    """
    Borrado de tlmyVartypes TODAS
    """    
   
    tttd.delete();
    
         
    """
    print("Arranco generacion de variables...")
    
    for i in range(0, 1500):
        #Variable con funcion
        tlv, created = TlmyVarType.objects.get_or_create(code="AV"+i.__str__(), 
                                                 description="AV"+i.__str__(),
                                                 satellite=sat,
                                                 varType=ltypeFloat,
                                                 position=i,
                                                 subPosition=0,
                                                 bitsLen=8,
                                                 frameType=ft,
                                                 subsystem=ss,
                                                 calibrationMethod=linealCalibration,
                                                 unitOfMeasurement=um,
                                                 ctype=ct)
        
        tlv.save()
        if created:
            if created:
                coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                                 value=0.005237,
                                                                 tlmyVarType=tlv)
                coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                                 value=0.0,
                                                                 tlmyVarType=tlv)
        pass
    
    for i in range(1500,1500+1180):
        #Variables sin metodo de calibracionresto 20 que son las ya configuradas
        tlv, created = TlmyVarType.objects.get_or_create(code="AV"+i.__str__(), 
                                                 description="AV"+i.__str__(),
                                                 satellite=sat,
                                                 varType=ltypeInteger,
                                                 position=i,
                                                 subPosition=0,
                                                 bitsLen=8,
                                                 frameType=ft,
                                                 subsystem=ss,
                                                 unitOfMeasurement=um,
                                                 ctype=ct)
        
        tlv.save()
    
        
    
    for i in range(0, 300):
        #Variables extraccion de bits
        tlv, created = TlmyVarType.objects.get_or_create(code="AVB"+i.__str__(), 
                                                 description="AVB"+i.__str__(),
                                                 satellite=sat,
                                                 varType=ltypeboolean,
                                                 position=i,
                                                 subPosition=i%8,
                                                 bitsLen=1,
                                                 frameType=ft,
                                                 subsystem=ss,
                                                 unitOfMeasurement=um,
                                                 ctype=ct)
        
    
    
    """
    print("Proceso terminado")
        
        
    #Toda la historia borrada
    
    
    