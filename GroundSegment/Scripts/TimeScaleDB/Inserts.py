'''
Created on 21 jun. 2020

@author: pablo
'''


#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDB/Inserts.py

import os, sys
from itertools import islice
from multiprocessing import Process, Pool
import random
from numpy import insert
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj_path = '/home/psoligo/git/GroundSegment/GroundSegment/'
#proj_path = '/home/pablo/git/GroundSegment/GroundSegment/'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from Simulators.DCSSimulator import satellite
from random import randint
import pytz
from datetime import datetime, timedelta
from numpy.random.mtrand import randint
from _datetime import timedelta

from django.db import connection
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.TlmyVar import TlmyVar
from GroundSegment.models.Log import Log
import numpy as np
import gc
from GroundSegment.models.Satellite import Satellite
import time
from django import db
import django
from django.db.models import Q

def efload(tstamp, period, groups):
    
    
    sats =  [Satellite.objects.get(code="BDSat1"), Satellite.objects.get(code="BDSat2"),  Satellite.objects.get(code="BDSat3")]
    
    tlvsl = []
    print("Generacion eficiente");
    for sat in sats:
        
        tvts = sat.tmlyVarType.all()
        afrom = tstamp #Fecha mas grande, asumo sincronizado todo!
        ato = afrom + timedelta(seconds=period)
        for i in range(5):
            
            for tvt in tvts:
                if randint(0, 4)==2:
                    fcv = int(round(np.sin(ato.timestamp())*10));
                else:
                    fcv = int(round(np.cos(ato.timestamp())*10));
                
                #g_time = time.time()
                tvar                = TlmyVar()
                tvar.code           = tvt.code
                tvar.tlmyVarType    = tvt
                tvar.tlmyRawData    = None
                
                
                
                #raw+datetime
                #l_time = time.time()
                #tvar.setValue(fcv, ato) 
                tvar.tstamp     = ato;
                tvar.calIValue = fcv;
                tvar.calSValue = "";
                tvar.calFValue = fcv;
                tvar.calBValue = False;
                #tvar.calIValue = fcv;
                #l_ftime =  time.time()
                tlvsl.append(tvar)
                
            ato = ato + timedelta(seconds=period)
                
        print("Satellite ", sat.code, "finalizado")
            
    return tlvsl
        
    


"""
def savetlmy(batch):
    for name, info in django.db.connections.databases.items(): # Close the DB connections
        django.db.connection.close()
    TlmyVar.objects.bulk_create(batch)   
"""    
    
    
def inserts(tvts, ttcount, lastts, tlvsl):
    period = 8
    groups = 4
    
    #5*6=media hora
    if len(tlvsl)==0:
        tlvsl = efload(lastts, period, groups);
    
    
    print("Por ingresar nuevo bloque datos")
    #ultimo paquete
    random.shuffle(tlvsl)
    
    normaltimes = []
    hipertimes  = []
    
    gc.collect()
    db.reset_queries()
    
    batch_size  = 1000 #(int)(len(tlvsl)/5)
    for tv in tlvsl:
        tv.id       = None
        
    TlmyVar._meta.db_table = "Telemetry_tlmyvar"
    start = time.time()
    TlmyVar.objects.bulk_create(tlvsl, batch_size)  
    end = time.time()
    normaltimes.append(end-start)
    
    for tv in tlvsl:
        tv.id       = None
    
    TlmyVar._meta.db_table = "Telemetry_htlmyvar"
    start = time.time()
    TlmyVar.objects.bulk_create(tlvsl, batch_size)  
    end = time.time()
    hipertimes.append(end-start)
   
    for tv in tlvsl:
        tv.tstamp   = tv.tstamp+timedelta(seconds=(period*groups+1))
        tv.id       = None
        
    ttcount+=len(tlvsl)
    
    print("Guardando medias de insercion, ttcount en ", ttcount, "normal:", normaltimes, "hiper:", hipertimes)
   
    Log.create("LASTROWCOUNT", str(ttcount), str(ttcount),Log.INFORMATION).save()
    Log.create("TI-NORMTABLENN", sum(normaltimes)/len(tlvsl) , str(ttcount), Log.INFORMATION).save()
    Log.create("TI-HIPERTABLENN", sum(hipertimes)/len(tlvsl), str(ttcount), Log.INFORMATION).save()
    
    print("Bloque de datos ingresados!", max(tv.tstamp for tv in tlvsl))
    TlmyVar._meta.db_table = "Telemetry_tlmyvar"
    return ttcount, tlvsl
        
    

if __name__ == '__main__':
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    tvts = TlmyVarType.objects.filter(satellite__code__in = sats).values_list('pk', flat=True)
    #Log.objects.filter(~Q(code="LASTROWCOUNT")).delete()
    #Log.objects.all().delete()
    start = time.time()
    ttcount = TlmyVar.objects.count()
    end = time.time()
    TlmyVar._meta.db_table = "Telemetry_tlmyvar"
    #lastid = TlmyVar.objects.order_by('id').last().id
    lastts = TlmyVar.objects.order_by('tstamp').last().tstamp
    
    print("Ver cantidad de registros demoro: ", end-start)
    insert(tvts, ttcount, lastts)