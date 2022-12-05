'''
Created on 10 jun. 2019

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

from GroundSegment.models.Satellite import Satellite

import pytz
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__ == '__main__':
    
    sat = Satellite.objects.get(code="SACD")
    sat.ephems.all().delete()
    sat.propagations.all().delete()
    
    epoch = datetime(2015,5,15,16,43,0,0, tzinfo=pytz.UTC)
    
    for j in range(120*7):
        epoch = (epoch+timedelta(seconds=1)).replace(tzinfo=pytz.UTC)
        et = sat.eclipseElapsedTime(epoch)
        
        print("Time in, or before eclipse->",epoch, et);
    