'''
Created on 08-abr-2021

@author: pabli
'''

#python .\GroundSegment\Adapters\ISS\ISSAdapter.py


#SELECT last_value FROM "Telemetry_tlmyvartype_id_seq"
#ALTER SEQUENCE "Telemetry_tlmyvartype_id_seq" RESTART WITH 62;

import os; 
import sys;

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
os.chdir(proj_path)
os.chdir('..')

sys.path.append(os.getcwd())

import math
import datetime
import pytz
import signal
import sys

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from Adapters.ISS.CreateDefaultData import createDefaultData
from GroundSegment.models.SatelliteState import SatelliteState
from Adapters.ISS.issTelemetryClient import TelemetryStream
from time import sleep
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from Telemetry.models.TlmyVar import TlmyVar
from django.db.utils import IntegrityError
#pip install py-iss-telemetry


def convertDTime(v, mul):
  muls = [24,60,60];
  toAdd = math.floor(v);
  next = v-toAdd;
  if(len(str(toAdd)) == 1):
    strToAdd="0"+str(toAdd);
  else:
    strToAdd = str(toAdd);
  
  if(mul < len(muls)):
    sep = "/" if mul==0 else ":"
    return strToAdd+sep+convertDTime(next*muls[mul],mul+1);
  
  return strToAdd;
  
def convertTime(v, mul):
  muls = [24,60,60];
  toAdd = math.floor(v);
  _next = v-toAdd;
  
  strToAdd = str(toAdd)
  if(len(strToAdd) == 1):
    strToAdd ="0"+strToAdd;
    
  
  if(mul < len(muls)):
    if(mul==0):
      strToAdd = ""
      return strToAdd+convertTime(_next*muls[mul],mul+1); 
    else:
      return strToAdd+":"+convertTime(_next*muls[mul],mul+1);
   
  #Caso base
  return strToAdd;
  
stream = None

def run_program():  
  createDefaultData()
  iss = Satellite.objects.get(code="ISS")
  ttList = iss.tmlyVarType.all()
  stream=None
  opcodes = [ tt.code for tt in ttList ]
  
  try:
    i = 0
    while(True):
      if stream==None:
        stream = TelemetryStream(opcodes=opcodes)
      try:
        values = stream.get_tm_and_clear()
        #print("Values: ", len(values))
        for v in values:
          days = float(v["TimeStamp"])/24
          strtime = convertTime(days, 0)
          utcdt   = datetime.datetime.utcnow()
          dttime=  datetime.datetime.strptime(strtime,'%H:%M:%S').time()
          ftimestamp = datetime.datetime.combine(utcdt.date(), dttime, tzinfo=pytz.UTC)
          
          try:
            tvar = TlmyVar.create(telemetry_type=TlmyVarType.objects.get(code=v["name"]),
                                  value=float(v["CalibratedData"]),
                                  tstamp=ftimestamp);
          
            tvar.save()
            print("tstamp:", tvar.code, tvar.tstamp)
          except IntegrityError as ex:
            print("Error de integridad capurado")
        sleep(10)
        i=i+1
      except Exception as e:
        stream.disconnect()
        stream = None;
        
  finally:
    stream.disconnect()
    
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            if stream!=None:
              stream.disconnect()
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)
    
    
if __name__ == '__main__':
  original_sigint = signal.getsignal(signal.SIGINT)
  signal.signal(signal.SIGINT, exit_gracefully)
  run_program()
