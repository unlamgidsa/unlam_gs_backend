'''
Created on 28 de nov. de 2016

@author: pabli
'''

import os, sys


    
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet
from django.db import transaction
import threading
import time
from django.db import connection




if __name__ == '__main__':
    
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
    from GroundSegment.models.TlmyVarType import TlmyVarType
    
    #Consulto por la primera telemetrytype con funcion de calibracion
    
    tt = TlmyVarType.objects.exclude(calibrationMethod__isnull=True).first()
    
    ##aClass = tt.calibrationMethod.aClass
    ##aMethod = tt.calibrationMethod.aMethod
    tt.setValue(11)
    ##from Calibration.GenericCalibration import *
    tt.setValue(12)
    
    #print(globals())
   
    
    
    
    
    