# -*- coding: utf-8 -*-
'''
Created on 2 jul. 2020

@author: pablo
'''


import psycopg2
import sys
import os
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj_path = '/home/pablo/git/GroundSegment/GroundSegment/'
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

from GroundSegment.models.Satellite import Satellite
import time
from django.db import connections
from django.db.utils import OperationalError
import matplotlib.pyplot as plt
import matplotlib as mpl

styles = ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 
              'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 
              'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 
              'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 
              'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']

if __name__ == '__main__':
    
    con = None
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    tvts = TlmyVarType.objects.filter(satellite__code__in = sats).values_list('pk', flat=True)
    
    #con = psycopg2.connect(host='192.168.1.7', database="DBGS_RESE", user='postgres', password='postgres')
    con = connections['default']
    hypert = []
    normat = []
    
    for i in range(30):
        start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).first().tstamp
        end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).last().tstamp
        arange    = randint(3,15)
        tvtid = tvts[randint(0, len(tvts))]
       
    
        #consultas tiempo real
        afrom    = end_date-timedelta(minutes=arange)
        ato      = end_date; 
        
        queryn = """
            SELECT *
            FROM "Telemetry_tlmyvar" 
            WHERE "Telemetry_tlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                    "Telemetry_tlmyvar"."tlmyVarType_id" = {}
            ORDER BY "Telemetry_tlmyvar".tstamp DESC;
        """.format(afrom, ato, tvtid)
        
        #print(queryn)
        
        
        queryh = """
            SELECT *
            FROM "Telemetry_htlmyvar" 
            WHERE "Telemetry_htlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                    "Telemetry_htlmyvar"."tlmyVarType_id" = {}
            ORDER BY "Telemetry_htlmyvar".tstamp DESC;
        """.format(afrom, ato, tvtid)
        #print(queryh)
        cur = con.cursor()
        cur.execute("""Select * from "GroundSegment_satellite" """)
        print("Query de connexion");
        cur.close()
        
        
        cur = con.cursor()
        start = time.time()
        cur.execute(queryh)
        fa = cur.fetchall()
        end = time.time()
        print("Query Hypertabla ",end-start, len(fa));
        hypert.append(end-start)
        cur.close()
      
        cur = con.cursor()
        start = time.time()
        cur.execute(queryn)
        fa = cur.fetchall()
        end = time.time()
        print("Query Normal ",end-start, len(fa));
        normat.append(end-start)
        cur.close()
        

        
    #plots
    ss = styles[randint(len(styles))]
    mpl.style.use(ss)
    print("Style, ", ss);
    
    plt.plot(normat, 'r', label='Tabla Regular');
    plt.plot(hypert, 'b', label='Hipertabla');
    plt.title(label="tiempo consultas historicas")
    #plt.xlabel(cantidadreg)
    #plt.ylabel(seg)
    plt.legend()
    plt.show()
        
   
    
    

    
        

