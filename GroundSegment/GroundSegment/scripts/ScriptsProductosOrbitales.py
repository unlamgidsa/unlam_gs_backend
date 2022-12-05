'''
Created on Mar 13, 2017

@author: ubuntumate
'''


import os, sys
from django.utils.timezone import pytz


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.utils import timezone
from datetime import timedelta

from GroundSegment.models.Sitio import Sitio
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.PassGeneration import PassGeneration
from datetime import datetime


if __name__ == '__main__':
    

    sat = Satellite.objects.get(code="ISS")
    sat.getEclipses(datetime(2017,3,8,23,0).replace(tzinfo=pytz.UTC), datetime(2017,3,8,23,0).replace(tzinfo=pytz.UTC)+timedelta(hours=12))

