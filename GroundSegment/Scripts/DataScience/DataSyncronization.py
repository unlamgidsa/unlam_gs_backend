'''
Created on 05-mar-2021

@author: pabli
'''

import os; 
import sys; 
from rest_framework import status
from datetime import datetime
import requests
from Scripts.DataScience.DSUtils import getProjectPath



BASE_DIR = getProjectPath()
os.chdir(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)

import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.db import connection
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyRawData import TlmyRawData
from django.core.exceptions import ObjectDoesNotExist
from Telemetry.models.TlmyVarType import TlmyVarType

def rawDataSyncronization():
  from Utils.PktsHelpers import sendJsonDataPkt
  
  
  apiurl= "http://127.0.0.1:8000/TlmyRawData/"
  user='sa'
  password='elperroverde05'
  sat = Satellite.objects.get(code="TITA")
  sendsession = requests.Session()
  #TODO replace with values from db.
  sendsession.auth = (user, password)
  sendsession.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json',})
  
  
  
  max_raw_source = TlmyRawData.objects.filter(satellite=sat).order_by('-pktdatetime').first()
  
  diff_raws = TlmyRawData.objects.using('production').filter(satellite=sat, pktdatetime__gt=max_raw_source.pktdatetime).order_by('pktdatetime')
  
  
  for r in diff_raws:
    try:
      res = sendJsonDataPkt(apiurl,
                          r.capturedAt , #captureddt
                          r.pktdatetime, #packet
                          sat.noradId, 
                          r.getBlob().hex(), 
                          r.getBlob().hex(), 
                          False, 
                          "SYNC",
                          sendsession)
      
      
      if res.status_code==status.HTTP_409_CONFLICT:
          print("Duplicated", res)
          
      elif res.status_code==status.HTTP_201_CREATED:
          print("syncronizated", r.pk, res)
          
      else:
          print("Packet isn't accepted", res)
      
    except Exception as e:
        print("Exception sending data to rest service ", e);
        #else:
                    
  print("fin raw data syncronization")
  
  
  

if __name__ == '__main__':
  
  
  rawDataSyncronization();
  #ISSSyncronization();
  
  
    
  
  