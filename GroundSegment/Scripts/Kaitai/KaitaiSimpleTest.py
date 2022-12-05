'''
Created on 10-jun-2021

@author: pabli
'''

from GroundSegment.celery import loadDjangoApp
import importlib
loadDjangoApp()
from Telemetry.models.TlmyRawData import TlmyRawData

import re
import functools
from Scripts.Kaitai.KaitaiStructs import Bugsat1
from datetime import timedelta, datetime

if __name__ == '__main__':
    rds = TlmyRawData.objects.filter(satellite__code="TITA").order_by('-pktdatetime')[0:100];
    pos = 9

    for rd in rds:
      try:
        b = Bugsat1.from_bytes(rd.getBlob().tobytes())

      #raw = bindata[pos:pos+4]
      #raw = unpack('>I', raw)[0]
      
        raw = b.ax25_frame.payload.ax25_info.beacon_type.rtc_s
        basedate = datetime(1970,1,1)
        delta = timedelta(seconds=raw)
        pktdt = basedate+delta
        print(pktdt, raw)
      except:
        print("Error paquete")
      #parece que el real time clock no funciona
      #print(b.ax25_frame.payload.ax25_info.beacon_type.rtc_s)
  
    print("Fin de programa")
    
