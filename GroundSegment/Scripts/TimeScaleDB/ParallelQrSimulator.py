'''
Created on 21 jun. 2020

@author: pablo
'''
#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDB/ParallelQrSimulator.py
import os, sys


#proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(proj_path)
proj_path = '/home/psoligo/git/GroundSegment/GroundSegment/'
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
import numpy as np
from Scripts.TimeScaleDB.Inserts import inserts
from django.db.models import Q
def qry(rt, start_date, end_date, amount, tvts, table, query, type, returnl):
    #155544529
    con = psycopg2.connect(database=settings.DATABASES['default']['NAME'], 
                           user= settings.DATABASES['default']['USER'], 
                           password= settings.DATABASES['default']['PASSWORD'], 
                           host=settings.DATABASES['default']['HOST'], 
                           port=settings.DATABASES['default']['PORT'])

    con.autocommit=True
    np.random.seed()
    
    #Ajuste por timezone...
    start_date = start_date - timedelta(hours=3)
    end_date   = end_date  - timedelta(hours=3)
    
    cur = con.cursor()
    acum = 0
    for i in range(amount):
        tvtid       = tvts[np.random.randint(0, len(tvts))]
        arange      = np.random.randint(10,50)
            
        if rt:
            afrom    = end_date-timedelta(minutes=arange)
            ato      = end_date; 
        else:
            if (end_date-start_date).seconds>arange:
                delta       = (end_date-start_date)
            else:
                delta       = (end_date-timedelta(minutes=arange))-start_date
            randomsecs  = np.random.randint(1, delta.seconds)
            afrom       = start_date + timedelta(seconds=randomsecs)
            ato         = afrom + timedelta(minutes=arange)
            
        
        #print(rt, afrom, ato, tvtid)
        qr = query.format(table, table, afrom, ato, table, tvtid, table)
        cur.execute(qr)
        cur.fetchall()
        acum += cur.rowcount
        #print("Resultado->", rseed, afrom, ato, type, cur.rowcount)
        #print(qr)
        
    cur.close()
    con.commit()
    con.close()
    print("Media de registros obtenidos ",acum/amount)

    return returnl.append(acum/amount)

if __name__ == '__main__':
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    ttvts = TlmyVarType.objects.filter(satellite__code__in = sats)
    tvts  = ttvts.values_list('pk', flat=True)
    plainquery = """
                    SELECT 1
                    FROM "{}" 
                    WHERE "{}"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}' AND
                            "{}"."tlmyVarType_id" = {}
                    ORDER BY "{}".tstamp DESC;
                 """
    agrqueryh = """
                    SELECT max("calIValue"), min("calIValue"), avg("calIValue")
                    FROM "{}"
                    WHERE "{}"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}'
                    AND "{}"."tlmyVarType_id" = {}
                    GROUP BY time_bucket('12m', tstamp);
               """
               
    agrqueryn = """
                    SELECT max("calIValue"), min("calIValue"), avg("calIValue")
                    FROM "{}"
                    WHERE "{}"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}'
                    AND "{}"."tlmyVarType_id" = {}
                    GROUP BY round(date_part('epoch', tstamp)/(12*60))
    
                """
    
    
    
    process = []
    cr      = 0
    amount  = 50
    cpro    = 3
    nro     = 0
    #Log.objects.filter(~Q(code="LASTROWCOUNT")).delete()
    
    """
    log = Log.objects.filter(code="LASTROWCOUNT").order_by('id').last()    
    if log==None:
        cr = 0
    else:
        cr = int(log.description)
    """
    cr      = TlmyVar.objects.count()
    Log.create("LASTROWCOUNT", str(cr), str(cr),Log.INFORMATION).save()
    print("Cantidad de registros obtenida:", cr)
    lastts  = TlmyVar.objects.order_by('tstamp').last().tstamp
    start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).order_by('tstamp').first().tstamp
    end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).order_by('tstamp').last().tstamp
    tlvars = []
    try:
        while(True):
            cr, tlvars = inserts(ttvts, cr, lastts, tlvars)
            
            #start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).first().tstamp
            #end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).last().tstamp
            end_date = max(tv.tstamp for tv in tlvars)
            print("Q Rango Start date->", start_date)
            print("Q Rango End date->", end_date)
            manager = Manager()
            l = manager.list()
            #(start_date, end_date, amount, tvts):
            sim = [  
                     ("Telemetry_htlmyvar", plainquery, True, "SE-HIPERTABLENN", "hipertabla tiempo real", l),
                     ("Telemetry_tlmyvar", plainquery, True,"SE-NORMTABLENN", "tabla normal tiempo real", l),
                     ("Telemetry_htlmyvar", plainquery, False,"SE-HISTHIPERTABLENN", "hipertabla historico", l),
                     ("Telemetry_tlmyvar", plainquery, False,"SE-HISTNORMTABLENN", "tabla normal historico", l),
                     ("Telemetry_htlmyvar", agrqueryh, False,"SE-AGRHIPERTABLENN", "hipertabla agregada", l),
                     ("Telemetry_tlmyvar", agrqueryn, False,"SE-AGRNORMALTABLENN", "tabla normal agregada", l),]
                     
            for s in sim:
                for conn in connections.all():
                    conn.close()
                process = []
                start = time.time()
                
                for cp in range(cpro):
                    p = Process(target=qry, args=(s[2], start_date, end_date, amount, tvts, s[0], s[1], s[4], s[5]))
                    p.start()
                    process.append(p);
                    
               
                for p in process:
                    p.join()
                 
                """   
                for e in l:
                    print("Procesos terminados media de elementos consultados ", e)
                """    
                end = time.time()
                print(s[0], s[3], amount*cpro, 'consultas', end-start);
                #La primera medicion se descarta por ruidosa...
                if nro>2:
                    Log.create(s[3], str((end-start)/(amount*cpro)), str(cr), Log.INFORMATION).save()
            
            print("Medicion: ", nro)
            nro = nro + 1; 
    except KeyboardInterrupt:
        for p in process:
            p.join()        
        
    
    
    