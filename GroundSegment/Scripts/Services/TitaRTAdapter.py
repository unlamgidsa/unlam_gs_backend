'''
Created on 22 nov. 2018

@author: psoligo

'''


import os, sys, time


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from Telemetry.tasks import TitaAdapter

if __name__ == '__main__':
    
    TitaAdapter()