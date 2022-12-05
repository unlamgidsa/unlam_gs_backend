'''
Created on 30 de jul. de 2017

@author: pabli
'''



import os, sys

from struct import unpack



proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.utils import timezone
from datetime import timedelta, datetime

from GroundSegment.models.Sitio import Sitio
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.PassGeneration import PassGeneration
from GroundSegment.models.UHFRawData import UHFRawData
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TlmyVar import TlmyVar

PosFrameCommand         = 0
LenFrameCommand         = 1

PosFrameLen             = PosFrameCommand+LenFrameCommand
LenFrameLen             = 4

PosDataRate             = PosFrameLen+LenFrameLen
LenDataRate             = 4

PosModuluationNameLen   = PosDataRate+LenDataRate 
LenModuluationNameLen   = 1

PosModulationName       = PosModuluationNameLen+LenModuluationNameLen
LenModulationName       = 0

PosRSSI                 = PosModulationName+LenModulationName 
LenRSSI                 = 8

PosFrequency            = PosRSSI+LenRSSI
LenFrequency            = 8

PosPktLen               = PosFrequency+LenFrequency
LenPktLen               = 2

def is_set(x, n):
    return x & 2**n != 0 

def getPktPayload(chunk):
    
    
    framecommand = unpack("<B",chunk[PosFrameCommand:PosFrameCommand+LenFrameCommand])[0] 
    frameLength  = unpack("<I",chunk[PosFrameLen:PosFrameLen+LenFrameLen])
    datarate     = unpack("<I",chunk[PosDataRate:PosDataRate+LenDataRate])
    modulationnamelen = (unpack("<B",chunk[PosModuluationNameLen:PosModuluationNameLen+LenModuluationNameLen]))[0]
    modulationname    = chunk[PosModulationName:PosModulationName+modulationnamelen] 
    PosRSSI           = PosModulationName+modulationnamelen 
    rssi              = unpack("<d", chunk[PosRSSI:PosRSSI+LenRSSI])
    PosFrequency        = PosRSSI+LenRSSI
    freq                = unpack("<d", chunk[PosFrequency:PosFrequency+LenFrequency])
    PosPktLen           = PosFrequency+LenFrequency
    pktLen             = unpack("<H",  chunk[PosPktLen:PosPktLen+LenPktLen])
    PosUtcTime = PosPktLen+pktLen[0]
    LenUtcTime = 4
    
    PosPayload = PosPktLen+int(LenPktLen)
    ax25 = chunk[PosPayload:PosPayload+pktLen[0]]
    
    
    destination  = ax25[0:7]
    asource      = ax25[7:7+7]
    control      = ax25[7+7:7+7+1]
    protocol     = ax25[7+7+1:7+7+1+1]
    
    vardataoffset = 7+7+1+1
    payload = ax25[ vardataoffset: ]
                                    
    return payload

if __name__ == '__main__':


    
    """
    Obtengo paquetes a decodificar.
    """
    uhfs = UHFRawData.objects.filter(dataLen__gt=32).exclude(source="SIMULATION")
    sat = Satellite.objects.get(code="FS2017")
    tvt = sat.tmlyVarType.all()
    print("paquetes, variable", len(uhfs), len(tvt))
    
    for bd in uhfs:
        bd.getBlob()
        payload = getPktPayload(bd.getBlob())
        
        
        start = datetime.now()
        
        for tt in tvt:
            if tt.bitsLen >= 8:
                #TODO Se debe terminar la decodificacion de booleanos
                bitLen_div =tt.bitsLen // 8
                if bitLen_div == 1:
                    raw = unpack("<B",  payload[tt.position:tt.position+bitLen_div])[0]
                else:
                    raw = unpack("<H",  payload[tt.position:tt.position+bitLen_div])[0]
            else:
                raw = is_set(payload[tt.position], tt.bitsLen)                                         
                     
            
            
            tvar = TlmyVar()
            tvar.code = tt.code
            tvar.tmlyVarType = tt
            tvar.setValue(raw, True)
            tvar.save()
        
        print((datetime.now()-start).total_seconds())
        
            