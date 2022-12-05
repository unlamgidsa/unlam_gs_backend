'''
Created on 1 abr. 2020

@author: pablo
'''
from GroundSegment.celery import loadDjangoApp
from Scripts.Kaitai.__Bugsat import __Bugsat1


loadDjangoApp()

from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.FrameType import FrameType

if __name__ == '__main__':
        #TlmyVar.objects.filter(tlmyVarType__satellite__code="TITA").first()
    sub = SubSystem.objects.all().first()
    um = UnitOfMeasurement.objects.get(code="(D)")
    sat = Satellite.objects.get(code="TITA")
    ft = FrameType.objects.get(description="TITA_BEACON")
    rd = TlmyRawData.objects.filter(satellite__code="TITA").last();
    bp = __Bugsat1.from_bytes(rd.getBlob().tobytes())
    offset = 70 - 56
    for name, position, atype in bp.tlmyinfo:
        print(name, position, atype)
        
        if(atype!=None):
            ctype = CType.objects.get(tag=atype)
            
            tlv, created = TlmyVarType.objects.get_or_create(code=name, satellite=sat)
            
            tlv.description = tlv.code
            tlv.position=offset+position
            tlv.subPosition=0
            tlv.bitsLen=ctype.length*8
            tlv.subsystem=sub
            tlv.unitOfMeasurement=um
            tlv.ctype=ctype
            tlv.frameType = ft
            
            if (ctype.tag in ["u4be", "s4be", "s2be"]):        
                tlv.varType=TlmyVarType.INTEGER
                
            elif(ctype.tag in ["u", "u1"]):
                tlv.varType=TlmyVarType.STRING
                pass
            else:
                tlv.varType=TlmyVarType.FLOAT
            
            #tlv.delete()
            tlv.save()
        