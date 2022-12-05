'''
Created on 02-mar-2021

@author: pabli
'''

import os; 
from Scripts.Utils import getProjectPath

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
# This is so Django knows where to find stuff.

#sys.path.append(proj_path)
# This is so my local_settings.py gets loaded.



#from datetime import datetime, timedelta
from django.utils.timezone import utc
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType
from GroundSegment.models.Satellite import Satellite
from django.db.models import F
from django.db.models import Count

if __name__ == '__main__':
  
  
  vars = ["fine_gyro_x", "fine_gyro_y", "fine_gyro_z"]
  sat = Satellite.objects.get(code="TITA")
  rdatas = sat.rawdatas.all()
  batch = []
  for var in vars:  
    tt = TlmyVarType.objects.get(code=var)
    tt.tlmyVars.all().delete()
    
    
    for r in rdatas:
      try:
        var = TlmyVar.create(raw=r, telemetry_type=tt)
        batch.append(var)
        if(len(batch)>1000):
          TlmyVar.objects.bulk_create(batch)
          print("Var ", var.tstamp, "salvada")
          batch = []
        #print("guardado:", var.pk, var.code)
      except Exception as ex:
        print(ex)
      
      
  
  print("Fin")
  
  