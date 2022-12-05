'''
Created on Jan 15, 2017

@author: ubuntumate
'''

import os, sys

from _struct import unpack
from asyncio.tasks import sleep

sys.path.append('C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment')
#sys.path.append('/home/ubuntumate/git/GroundSegment/GroundSegment/')

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet
from django.db import transaction
import threading
import time
from django.db import connection
import psycopg2


n = 0
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

from datetime import datetime
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Sitio import Sitio

"""
Se importan Sitio, Satellite, y se define una fecha
Todo esto luego lo ingresa el operador seleccionando.
"""
sat = Satellite.objects.get(code="FS2017")
st = Sitio.objects.get(name="ETC")
n1 = '2019/9/2 00:05:16'

"""
Se ejecuta el metodo que calcula la pasada (Sitio/getPass)
"""
st.getPass(sat, n1) 





