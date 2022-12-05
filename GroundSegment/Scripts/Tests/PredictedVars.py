'''
Created on 19 jun. 2019

@author: pablo
'''

import os, sys, time
from _datetime import datetime, timedelta



proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from Calibration.SACDCalibration import SACDCalib
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.TlmyRawData import TlmyRawData
from GroundSegment.models.Satellite import Satellite
from CODS.models import Ephemeride
if __name__ == '__main__':
    
    
    
    sat = Satellite.objects.get(code="SACD")
    rawid = sat.rawdatas.first().id
    sc = SACDCalib()
    
    
    tvt = TlmyVarType.objects.get(code="vBatAverage(E)")
    eet = TlmyVarType.objects.get(code="eclipsedElapsedTime")
    
    #sc.vBatAveragePredicted(tvt, rawid)
    sc.eclipseElapsedTime(tvt, rawid)
    
    