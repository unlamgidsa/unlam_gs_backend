'''
Created on 9 may. 2019

@author: psoligo
'''

import gzip

from Utils.PktsHelpers import  sendJsonDataPkt
from datetime import datetime, timedelta
from struct import unpack
from dateutil import tz


APIURL = "http://127.0.0.1:8000/TlmyRawData/"
def sendSACDChunk(chunk):
    try:
        dtn = datetime.utcnow()
        #La fecha hora del packet la debo extraer del CDH Time...
        secs = unpack('>I', chunk[100:104])[0] 
        basedate = datetime(1980,1,6,0,0,0)
        pktdt = (basedate+timedelta(seconds=secs)).replace(tzinfo=tz.tzutc())
    
        #las tramas son de 4000 bytes, que tal si leemos asi?
        sendJsonDataPkt(APIURL, dtn , pktdt, "SACD", chunk.hex(), chunk.hex(), False, "FILE")
        #SendSACDPacket(pktdt, "FROMFILE", strm.hex(), False)
    except Exception as ex:
        print("Error Sending SACDCHUNK", ex)

if __name__ == '__main__':
    FRAMELEN = 4000
    
    filename = '/home/psoligo/git/GroundSegment/GroundSegment/Telemetry/ProcessedTlmy/SAC-D/CGSS_20150530_090200_10020150530084615_SACD_HKTMST.bin.gz'
    cf = gzip.open(filename, 'rb')
    
    strm = cf.read(FRAMELEN)
    while strm!='':
        sendSACDChunk(strm)
        strm = cf.read(FRAMELEN)
    #strm = cf.read(FRAMELEN)
    #sendSACDChunk(strm)
    
    
    cf.close()
                
    