'''
Created on 18 jul. 2020

@author: pablo
'''



#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDB/HistQr.py
import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj_path = '/home/pablo/git/GroundSegment/GroundSegment/'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from random import randint
import pytz
from datetime import datetime, timedelta
from numpy.random.mtrand import randint
from _datetime import timedelta

from django.db import connections
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.TlmyVar import TlmyVar
from GroundSegment.models.Log import Log
import numpy as np

from GroundSegment import settings
from GroundSegment.models.Satellite import Satellite
import time
from multiprocessing import Process, Manager
import psycopg2
import random
from django.db import transaction, DatabaseError

from django.db.models import Q

if __name__ == '__main__':
    
    
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    tvts = list(TlmyVarType.objects.filter(satellite__code__in = sats))#.values_list('pk', flat=True)
    
    n = 5000
    
    period = 8
    
    con = psycopg2.connect(database=settings.DATABASES['default']['NAME'], 
                           user= settings.DATABASES['default']['USER'], 
                           password= settings.DATABASES['default']['PASSWORD'], 
                           host=settings.DATABASES['default']['HOST'], 
                           port=settings.DATABASES['default']['PORT'])

    #con.autocommit = True
               
    start = time.time()
    #ttcount = 46059999
    ttcount = TlmyVar.objects.count()
    
    end = time.time()
    print("Ver cantidad de registros demoro: ", end-start, ttcount)
    np.random.seed()
    
    lastts = TlmyVar.objects.order_by('tstamp').last().tstamp + timedelta(seconds=period)  
    #lastts =  datetime(2020, 1, 1, 4, 7, 19, 0, pytz.UTC) #datetime.strptime('2020-01-01 04:07:19', '%Y-%m-%d %H:%M:%S'). #2020-01-01 04:07:19+00:00
    query = """insert into "Telemetry_tlmyvar" 
                       ("code", "rawValue", "calIValue", "calFValue", "calBValue", "calSValue", "created", "tstamp", "outlier", "tlmyVarType_id", "UnixTimeStamp") 
                       values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for conn in connections.all():
        conn.close()
    cur = con.cursor()
    while ttcount<150000000:
        start = time.time()
        data = []
        for tvt in tvts:
            ri = np.random.randint(1, 100)
            #Code, rawvalue, calIValue, calFValue, calBValue, calSValue, created, tstamp, outlier, tlmyVarType_id, UnixTimeStamp, null
            params = (tvt.code, ri, ri, float(ri), True, str(ri), str(datetime.utcnow()), str(lastts), False, tvt.pk, lastts.timestamp()*1000)
            data.append(params)
            #print("Vamos a insertar ", params)
            #cur.execute(query, params) 
        
        print("Insertando...")  
        
        for i in range(0, len(data), n):
            cur.executemany(query, data[i:i + n])
            con.commit()
            #time.sleep(1)
        
        #         
        #cur.executemany(query, data) 
            #print("Insercion ok")           
            
        ttcount+=len(tvts)    
        lastts = lastts+timedelta(seconds=period)   
        print("Fin de bloque,", lastts, ttcount)
        end = time.time()
        print("El bloque demoro: ", end-start)
        #break
    #TlmyVar.objects.order_by('id').last().delete()
    
            
            
            