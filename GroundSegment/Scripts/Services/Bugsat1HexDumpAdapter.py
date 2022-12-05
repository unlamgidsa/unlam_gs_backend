'''
Created on 10 jun. 2021

@author: pablo
'''

import os, sys, time
import pytz
from datetime import datetime, timedelta
import requests
from rest_framework import status
from Scripts.DSUtils import getProjectPath

#

BASE_DIR = getProjectPath()
os.chdir(BASE_DIR)

import sys; 
print('%s %s' % (sys.executable or sys.platform, sys.version))
os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User
from Telemetry.tasks import SendTitaPacket

from Utils.PktsHelpers import sendJsonDataPkt
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVar import TlmyVar


def isendJsonDataPkt(apiurl, dt, pktdt, source, data, payload, rt, tag, session):
  try:
    
    #SendTitaPacket
    res = sendJsonDataPkt(apiurl,
                          dt , #captureddt
                          pktdt, #packet
                          source, 
                          data, 
                          payload, 
                          rt, 
                          tag,
                          sendsession)
    
    
    if res.status_code==status.HTTP_409_CONFLICT:
        print("Duplicated", res)
    elif res.status_code==status.HTTP_201_CREATED:
        print("Accepted", res)
    else:
        print("Packet isn't accepted", res)
        
    
  
  except Exception as e:
    print("Exception sending data to rest service ", e);
  #else:


if __name__ == '__main__':
  
  os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  pf = open("../Telemetry/PendingTlmy/Tita/bugsat1.hex", "rt");
  pkt = None
  
  raws = TlmyRawData.objects.filter(tag="UNGS")
  TlmyVar.objects.filter(tlmyRawData__in=raws)
  TlmyVar.objects.filter(tlmyRawData__in=raws).delete()
  raws.delete()
  
  sendsession = requests.Session()
  #TODO replace with values from db.
    
  sendsession.auth = ("sa", "")
  sendsession.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json',})
    
  recsession = requests.session()
  
  dt_base = datetime(2021,5,17,20,13,38)
  
  #apiurl = "http://127.0.0.1:8000/TlmyRawData/"
  apiurl = "http://10.10.203.4:8001/TlmyRawData/"
  #=>apiurl, dt, pktdt, source, data, payload, rt, tag, session
  lines = pf.readlines()
  offset = 42.001
  for l in lines:
      v = l.split(":")
      nm  = v[0]
      if(nm=="0000"):
        if not (pkt==None):
          pkt = pkt.replace(" ", "").replace('\n', "")
          print("Enviando: ", pkt)
          isendJsonDataPkt(apiurl, 
                          datetime.utcnow().replace(tzinfo=pytz.utc), 
                          dt_base+timedelta(seconds=offset), 
                          "40014", 
                          pkt, 
                          pkt, 
                          False, 
                          "UNGS", 
                          recsession)
          #print("Paquete completo: ", pkt.upper())
        pkt = v[1] 
      else:
        pkt += v[1]
        
  
  pkt = pkt.replace(" ", "").replace('\n', "")
  print("Enviando: ", pkt)   
  
  isendJsonDataPkt(apiurl, 
                  datetime.utcnow().replace(tzinfo=pytz.utc), 
                  dt_base+timedelta(seconds=60+offset), 
                  "40014", 
                  pkt, 
                  pkt, 
                  False, 
                  "UNGS", 
                  recsession)
  
        
  #print("Paquete completo: ", pkt.upper())
  #=>isendJsonDataPkt(apiurl, dt, pktdt, source, data, payload, rt, tag, session)
          
  #SendTitaPacket(datetime.utcnow(), "UNLAM-GS", pkt.upper(), True)
  pf.close()
  
  
  """
  
  """
  
                                   
   
        