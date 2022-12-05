'''
Created on 03-mar-2021

@author: pabli
'''

import os; 
from datetime import datetime
import pytz



BASE_DIR = "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
os.chdir(BASE_DIR)

import sys; 
print('%s %s' % (sys.executable or sys.platform, sys.version))
os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.utils.timezone import utc
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from GroundSegment.models.Satellite import Satellite
from django.db.models import F
from django.db.models import Count
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.SubSystem import SubSystem

if __name__ == '__main__':
    
    
  batch = []
  line = ""
  state, created      = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
  state.save()
  satellite, created  =Satellite.objects.get_or_create(code="LASP", description="LASP", noradId=0, state=state)
  satellite.save()
  um, created = UnitOfMeasurement.objects.get_or_create(code="C", description="Celsius")
  um.save()
  ct, created = CType.objects.get_or_create(code="unsigned 32 little-endian", format="<I", length=4)
  ct.save()
  ss, created = SubSystem.objects.get_or_create(code="THERMAL", description="THERMAL")
  ss.save()
  INTEGER = 0;
  FLOAT = 1;
  battemp, created = TlmyVarType.objects.get_or_create(code="BTemp",
                                                   description="Battery Temperature",
                                                     satellite=satellite,
                                                     varType=FLOAT,
                                                     position=0,
                                                     subPosition=0,
                                                     bitsLen=0,
                                                     subsystem=ss,
                                                     unitOfMeasurement=um,
                                                     ctype=ct)
  battemp.save()
  
  f = open("C:\\Users\\pabli\\Downloads\\Orig_LASP_telemetry_data\\BatteryTempCPV6Averaged.csv", "rt")
  line = f.readline()
  #yyyy-MM-dd'T'HH:mm:ss.SSS
  #2004-02-13 13:02:30
  battemp.tlmyVars.all().delete()
  line = f.readline()
  while(line!=""):
    
    vals = line.split(',');
    
    date = pytz.utc.localize(datetime.strptime(vals[0], '%Y-%m-%d %H:%M:%S'))
  
    value = float(vals[1])
    var = TlmyVar.create(value=value, tstamp=date, telemetry_type=battemp )
    batch.append(var)
    if(len(batch)>1000):
      TlmyVar.objects.bulk_create(batch)
      print("Var ", var.tstamp, "salvada")
      batch = []
    
    line = f.readline()
    
    
  
  f.close()
  
  print("Fin de programa")
  
  