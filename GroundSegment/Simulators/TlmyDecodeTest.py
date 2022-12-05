'''
Created on 25 de nov. de 2016

@author: pabli
'''

import os, sys

from _struct import unpack
from asyncio.tasks import sleep

sys.path.append('C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment')
#sys.path.append('/home/ubuntumate/git/GroundSegment/GroundSegment/')

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet
from django.db import transaction
import threading
import time
from django.db import connection
import psycopg2


n = 0
ROOT_DIR = BASE_DIR
#proj_path = "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
proj_path = ROOT_DIR
 #https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)


# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TmlyVar import TlmyVar
from GroundSegment.models.TlmyRawData import TlmyRawData
import struct
from Simulators.ax25 import printpacket
        
#1- 7 bytes - Destination Callsign
#2- 7 bytes - Source Callsign
#3- 2 bytes - Control Bytes
#4- Variable - Data bytes (Data sent by the OBC)
#5- 2 bytes - FCS (AX25 CRC)

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




if __name__ == '__main__':
    
    
    
    uhfs = TlmyRawData.objects.filter(id__gte=996, id__lte=1482)
    
    
    
    #uhfs = TlmyRawData.objects.filter(source="CUBESAT")
    
    for u in uhfs:
        
        barray = u.getBlob()
        print(barray)
        framecommand        = barray[PosFrameCommand:PosFrameCommand+LenFrameCommand]
        frameLength         = unpack("<I", barray[PosFrameLen:PosFrameLen+LenFrameLen])
        datarate            = unpack("<I", barray[PosDataRate:PosDataRate+LenDataRate])
        modulationnamelen   = barray[PosModuluationNameLen:PosModuluationNameLen+LenModuluationNameLen]
        
        LenModulationName   = modulationnamelen[0]
        
        modulationname      = barray[PosModulationName:PosModulationName+LenModulationName]     
        
        
        PosRSSI             = PosModulationName+LenModulationName 
        
        rssi                = unpack("<d",  barray[PosRSSI:PosRSSI+LenRSSI])
        
        PosFrequency        = PosRSSI+LenRSSI
        freq                = unpack("<d",  barray[PosFrequency:PosFrequency+LenFrequency])
        
        PosPktLen           = PosFrequency+LenFrequency
        print("BBBBB", barray[PosPktLen:PosPktLen+LenPktLen])
        
       
        pktLen             = unpack("<H",  barray[PosPktLen:PosPktLen+LenPktLen])
        
        
        
        print(framecommand, ", ", frameLength, ", ", datarate, ", ", modulationname, "rssi", rssi, "Freq ", freq, "PktLen", pktLen)
        
        
        PosUtcTime = PosPktLen+pktLen[0]
        LenUtcTime = 4
        
        PosPayload = PosPktLen+int(LenPktLen)
        ax25 = barray[PosPayload:PosPayload+pktLen[0]]
        
        
        destination = ax25[0:7]
        source      = ax25[7:7+7]
        control     = ax25[7+7:7+7+1]
        protocol    = ax25[7+7+1:7+7+1+1]
        

             
        vardataoffset = 7+7+1+1
        payload = ax25[ vardataoffset: ]
        
        tvts = TlmyVarType.objects.filter(satellite__code="FS2017")
        for tv in tvts:
            raw = unpack("<H",  payload[tv.position:tv.position+tv.bitsLen])
            tv.setValue(raw[0], True)
            
        time.sleep(1)
            
        #
        
        #print("str->", str)
        
            
    #uhfs = TlmyRawData.objects.filter(id_gte=996, id_lte=1482)
    
    """
    struct.pack('>I', 5000) # works fine
    >>>'\x00\x00\x13\x88'
    
    struct.pack('>I', 50000) # has a weird "P" variable which the documentation says shouldn't occur with Endian order.
    >>>'\x00\x00\xc3P'
    
    >>> ord('P')
    80
    >>> hex(80)
    '0x50'
    >>> 
    
    bytearray((0x00, 0x00, 0xc3, 0x50)) == struct.pack(">I", 50000)
    struct.pack('>I', 50000).encode("hex") '0000c350'
    
    """

    
    #datatype2 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 01 A7 00 B0 00 00 00 00 E7 00 EC 00 31 CC CC 39 02 98 01 BA 03 04 00 04 00 00 00 3D 00 DF 00 E7 01 00 00 00 00 00 00 00 00 7F 1F 62 00 13 00 13 00 13 00 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 AD 00 00 00 00 27 DF 0A BF 0A DF 0A 04 00 04 00 04 00 00 16 6B D3"
    #datatype2 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 01 B6 00 C0 00 00 00 00 E7 00 ED 00 32 CC CC 37 02 98 01 AD 03 04 00 04 00 00 00 3D 00 DF 00 E8 01 00 00 00 00 00 00 00 00 7F 1F 62 00 13 00 13 00 13 00 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 AD 00 00 00 00 27 DF 0A BF 0A DF 0A 04 00 04 00 05 00 00 16 88 7D "
    #datatype2 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 01 C5 00 D0 00 00 00 00 E6 00 ED 00 31 CC CC 39 02 98 01 B5 03 04 00 04 00 00 00 3D 00 DF 00 E8 01 00 00 00 00 00 00 00 00 7F 1F 62 00 13 00 13 00 13 00 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 AD 00 00 00 00 27 DF 0A DF 0A DF 0A 03 00 05 00 04 00 00 16 31 55"
    #datatype2 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 04 14 01 24 01 00 00 02 97 01 B5 03 04 00 04 00 00 00 3F 00 E1 00 E7 01 FA 75"
    #datatype3 = "E2 08 80 3C 38 98 E2 2A 16 14 F2 74 54 45 DA 66 6D 16 49 E6"
    """
    baDataType2 = bytearray.fromhex(datatype2)
    print(baDataType2)
    
    destination = baDataType2[0:7]
    source      = baDataType2[7:7+7]
    control     = baDataType2[7+7:7+7+1]
    protocol    = baDataType2[7+7+1:7+7+1+1]
    print("Destination", destination)
    print("Source", source)
    print("Control", control)
    print("Protocol", protocol)
    vardataoffset = 7+7+1+1
    payload = baDataType2[ vardataoffset: ]
    print("Payload len ", len(payload) )
    
    frametype = payload[0]
    print("Frametype ", frametype)
    
    resetcause = payload[69]
    print("resetcause", resetcause)
    
    
    MPPTmode = payload[74]
    print("MPPTmode ", MPPTmode)
    
    pkn1 = payload[1:3]
    #pkn2 = payload[2]
    
    
    print(unpack("<H", pkn1))
    #print(unpack(">I", pkn1)
    
    PAtemp = payload[29:29+2]
    iPaTemp = unpack("<H", PAtemp)
    print("PaTemp ", (iPaTemp[0]*0.32258) - 50)
    
    busV = payload[31:31+2]
    ibusV = unpack("<H", busV)
    print("Bus ", (ibusV[0]*0.016581))
    
    #<number position="41" type="short" name="BattV" unit="V" gain="0.001" offset="0"/>
    
    bat = payload[41:41+2]
    ibat = unpack("<H", bat)
    print("Bat ", (ibat[0]*0.001))
    
    
        
    bat = payload[41:41+2]
    ibat = unpack("<H", bat)
    print("Bat ", (ibat[0]*0.001))
    
    """
