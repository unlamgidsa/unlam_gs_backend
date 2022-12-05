from struct import unpack, pack
import json
import requests
from rest_framework import status


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



def DireWolfFile():
    def __init__(self, filename):
        f = fopen(filename, "rb")
    
    def nextpacket(self):
        pass

def ExtractFS2017AX25Payload(chunk):
    
    
    try:
        framecommand        = unpack("<B",chunk[PosFrameCommand:PosFrameCommand+LenFrameCommand])[0] 
        frameLength         = unpack("<I",chunk[PosFrameLen:PosFrameLen+LenFrameLen])
        datarate            = unpack("<I",chunk[PosDataRate:PosDataRate+LenDataRate])
        modulationnamelen   = (unpack("<B",chunk[PosModuluationNameLen:PosModuluationNameLen+LenModuluationNameLen]))[0]
        modulationname      = chunk[PosModulationName:PosModulationName+modulationnamelen] 
        PosRSSI             = PosModulationName+modulationnamelen 
        rssi                = unpack("<d", chunk[PosRSSI:PosRSSI+LenRSSI])
        PosFrequency        = PosRSSI+LenRSSI
        freq                = unpack("<d", chunk[PosFrequency:PosFrequency+LenFrequency])
        PosPktLen           = PosFrequency+LenFrequency
        pktLen              = unpack("<H",  chunk[PosPktLen:PosPktLen+LenPktLen])
        PosUtcTime          = PosPktLen+pktLen[0]
        LenUtcTime          = 4
        
        
        
        PosPayload = PosPktLen+int(LenPktLen)
        ax25 = chunk[PosPayload:PosPayload+pktLen[0]]
        
        
        destination  = ax25[0:7]
        asource      = ax25[7:7+7]
        control      = ax25[7+7:7+7+1]
        protocol     = ax25[7+7+1:7+7+1+1]
        
        #A8 A4 B0 AA AC 40 60 40 40 40 40 40 40 E1 03 F0 02 03 83 A5
             
        vardataoffset = 7+7+1+1 #16
        payload = ax25[ vardataoffset: ]
        
        pn = unpack("<H",  payload[1:3])
        frameTypeId = payload[0]
        if frameTypeId in [1,2,3,4,5,6,170]:
            return payload
        else:
            return None
    except Exception as e:
        #el paquete es mas corto de lo esperado?
        print(e);
        return None
    
#TODO: Pendiente usar esta funcion en lituanicasatAdapter
def sendJsonDataPkt(apiurl, dt, pktdt, source, data, payload, rt, tag, session):

         
    jdata = {}
    
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    """
    jdata['capturedAt']     = dt.isoformat()
    jdata['pktdatetime']    = pktdt.isoformat()
    jdata['source']         = source
    jdata['strdata']        = data
    jdata['strpayload']     = payload
    jdata['realTime']       = rt
    jdata['tag']            = tag
    jsondata                = json.dumps(jdata)
            
    #"{'pktdatetime': '1976-10-30T20:20:00Z', 'source': 'LITUANICASAT2', 'strdata': 'AAFFAA','realTime': true,'tag': 'DELETE'}"
    
    res = session.post(url=apiurl, data=jsondata);   
    ##res = requests.post(url=apiurl, headers=headers, data=jsondata)
    if res.status_code!=status.HTTP_201_CREATED:
        print("Error ",res.status_code)
    
    return res
       
     #logger.info(res.json()["errors"])
     #print(res.status_code, res.reason, res.json()["errors"])            

#TODO: Pendiente usar esta funcion en lituanicasatAdapter
#NO probado aun
async def AsyncSendJsonDataPkt(apiurl, dt, pktdt, source, data, payload, rt, tag, session):

         
    jdata = {}
    
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    """
    jdata['capturedAt']     = dt.isoformat()
    jdata['pktdatetime']    = pktdt.isoformat()
    jdata['source']         = source
    jdata['strdata']        = data
    jdata['strpayload']     = payload
    jdata['realTime']       = rt
    jdata['tag']            = tag
    jsondata                = json.dumps(jdata)
            
    #"{'pktdatetime': '1976-10-30T20:20:00Z', 'source': 'LITUANICASAT2', 'strdata': 'AAFFAA','realTime': true,'tag': 'DELETE'}"
      
    res = await session.post(url=apiurl, data=jsondata);   
    ##res = requests.post(url=apiurl, headers=headers, data=jsondata)
    if res.status_code!=status.HTTP_201_CREATED:
        print("Error ",res.status_code)
    
    return res
       
     #logger.info(res.json()["errors"])
     #print(res.status_code, res.reason, res.json()["errors"])            


        
    