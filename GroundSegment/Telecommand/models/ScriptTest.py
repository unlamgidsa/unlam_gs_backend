'''
Created on Aug 16, 2017

@author: ubuntumate
'''

import os, sys




proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.Satellite import Satellite
from .CommandType import CommandType
from .Command import Command
from .CommandParameter import CommandParameter
from .CommandTypeParameter import CommandTypeParameter
from datetime import datetime, timedelta





if __name__ == '__main__':
    fs2017 = Satellite.objects.get(code="FS2017")
    
    """
    ct = fs2017.getCommandType().get(code="startiMTQ")
    cmd = fs2017.newCommand(ct, datetime.utcnow()+timedelta(minutes=5))
    cmd.addParameters(0,0,0)
    fs2017.sendCommand(cmd)
    """
    
    #fs2017.sendDCommand("startiMTQ", datetime.utcnow()+timedelta(minutes=5), 100, 100, 100)
    
    fs2017 = Satellite.objects.get(code="FS2017")
    fs2017.sendRTCommand("beaconOBC", 5, 30)
    
    
    