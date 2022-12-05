'''
Created on 26 mar. 2020

@author: pablo
'''




from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.TlmyVarType import CType
from Telemetry.models.TlmyVarType import FrameType
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement

from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.TlmyVar import TlmyVar
from django.utils.timezone import datetime, now, timedelta, utc



    
   
def create_iss_base_data():
    #Se asume que ciertos datos maestros existen
    
    ss  = SatelliteState.objects.get(code="NOMINAL")
    
    iss, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)
    iss.save()
    ft, created = FrameType.objects.get_or_create(aid=500, description="ISS_ITelemetry", satellite=iss)
    ft.save()
    
    floatctype, created = CType.objects.get_or_create(code="float", format="<f", length=4);
    floatctype.save()
    
    strctype, created = CType.objects.get_or_create(code="str", format="c", length=25);
    strctype.save()
    
    floatissvars = [("Tranquility_ppO2", "NODE3000001|1"), ("Tranquility_ppCO2", "NODE3000003|1"), ("Destiny_lab_Pressure", "USLAB000058|1"),
                     ("Destiny_lab_Temp","USLAB000059|1"), ("Destiny_lab_ppO2","USLAB000053|1"), ("Destiny_lab_ppN2","USLAB000054|1"),
                     ("Destiny_lab_ppC02","USLAB000055|1"), ("QAir_Crewlock_Pressure","AIRLOCK000049|1"), ("QAir_EVA_Ox_Tank_Press","AIRLOCK000055|1"),
                     ("QAir_Nit_Tank_Press","AIRLOCK000057|1"), ("QAir_Ox_Tank_Press","AIRLOCK000056|1")]
    tlv = None
    for vn, code in floatissvars:
        
        if not tlv:
            position = 0
        else:
            position = tlv.position+tlv.ctype.length
        
        tlv, created = TlmyVarType.objects.get_or_create(code=vn,
                                                     description=vn,
                                                     satellite=iss,
                                                     varType=0,
                                                     position=position,
                                                     subPosition=0,
                                                     bitsLen=CType.objects.get(code="float").length,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(code="(D)"),
                                                     ctype=CType.objects.get(code="float"),
                                                     frameType=ft,
                                                     tag=code)
        
        tlv.save()


    

    
    
    
    
    
    
    
    """
    Continuar pasando la variables a telemetria

                (,, float),
                 ("Tranquility_FANSTATUS","NODE3000018", str),
                 
                 
                 ("Destiny_lab_PortFan","USLAB000064", str),
                 ("Destiny_lab_StarboardFan","USLAB000065", str),
                 ("Harmony_CoolantTemp","NODE2000006", str),
                 ("Harmony_FanStatus","NODE2000003", str),
                 
                 ("QAir_Vacuum_Exhaust_Valve","USLAB000063", str),
                 ("QAir_Vaccum_Resource_Valve","USLAB000062", str),
                 ("QAir_Pressure","AIRLOCK000054", float),
                 ("QAir_FanStatus","AIRLOCK000053", str),
                 
                 ("QAir_EVA_Oxygen_Tank_POS","AIRLOCK000050", str),
                 
                 ("QAir_Nitrogen_Tank_POS","AIRLOCK000052", str),
                 
                 ("QAir_Oxygen_Tank_POS","AIRLOCK000051", str),
                 
                 
                 ]
    """
    return iss.tmlyVarType.all()


    