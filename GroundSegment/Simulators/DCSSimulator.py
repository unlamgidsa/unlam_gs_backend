'''
Created on Jan 26, 2017

@author: ubuntumate
'''


import socket
import sys
import time
import struct
import datetime
from _datetime import timedelta
import os

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source = "SIMULATION"
satellite = "FS2017"
module = "TlmyCmdProcessor"

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.DCPPlatform import DCPPlatform
from GroundSegment.models.DCPData import DCPData 
from django.utils.timezone import datetime, now, timedelta, utc
import random

if __name__ == '__main__':
    
    while True:
        for d in DCPPlatform.objects.all():
            
            #(self, datetime,  precipitation, humidity, temp_max, temp_media, temp_min, atm_preasure):
            res = d.setData(utc, random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), random.randrange(0, 10), random.randrange(0,10))
            print("Dato DCS simulado insertado", res)
        time.sleep(60)
        
