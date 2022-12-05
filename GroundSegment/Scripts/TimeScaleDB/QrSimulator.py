'''
Created on 21 jun. 2020

@author: pablo
'''

#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDB/QrSimulator.py

##Ambas queries tiene que estar en el mismo script para asegurar que no se pisan 
##Trabajar ambas al mismo tiempo puede producir que algunas pruebas se ejecuten al mismo
##tiempo mientras que otras trabajen mas relajadas

import os, sys


#proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

if __name__ == '__main__':
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    tvts = TlmyVarType.objects.filter(satellite__code__in = sats).values_list('pk', flat=True)
    cr = 0;
    
    while(True):
        try:
            start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).first().tstamp
            end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).last().tstamp
            normaltabletimes = []
            hipertabletimes = []
            
            log = Log.objects.filter(code="LASTROWCOUNT").last()    
            #Baja siempre
            while cr == int(log.description):
                print("Esperando bloque de inserciones")
                time.sleep(10)
                log = Log.objects.filter(code="LASTROWCOUNT").last() 
                
                   
            cr = int(log.description)
            
            start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).first().tstamp
            end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).last().tstamp
            print("Q Rango Start date->", start_date)
            print("Q Rango End date->", end_date)
            
            
            for i in range(100):
                TlmyVar._meta.db_table = "Telemetry_tlmyvar"
                arange    = randint(3,15)
                tvtid = tvts[randint(0, len(tvts))]
            
                #consultas tiempo real
                afrom    = end_date-timedelta(minutes=arange)
                ato      = end_date; 
                
                query = """
                    SELECT *
                    FROM "Telemetry_tlmyvar" 
                    WHERE "Telemetry_tlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}'  AND
                            "Telemetry_tlmyvar"."tlmyVarType_id" = {}
                    ORDER BY "Telemetry_tlmyvar".tstamp DESC;
                """.format(afrom, ato, tvtid)
                avars = TlmyVar.objects.raw(query)
                start = time.time()
                avars._fetch_all()
                end = time.time()
                normaltabletimes.append(end-start)
                
                print("Result set len: ", len(avars));
                
                
                
                TlmyVar._meta.db_table = "Telemetry_htlmyvar"
                query = """
                    SELECT *
                    FROM "Telemetry_htlmyvar" 
                    WHERE "Telemetry_htlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}'  AND
                            "Telemetry_htlmyvar"."tlmyVarType_id" = {}
                    ORDER BY "Telemetry_htlmyvar".tstamp DESC;
                """.format(afrom, ato, tvtid)
        
                avars = TlmyVar.objects.raw(query)
                start = time.time()
                avars._fetch_all()
                end = time.time()
                hipertabletimes.append(end-start)
                              
               
                print("Result set len (Realtime): ", len(avars));
                #Ahora historico
                TlmyVar._meta.db_table = "Telemetry_tlmyvar"
                arange    = randint(3,15)
                normaltabletimeshist = []
                hipertablestimehist = []
                #100 consultas para test de velovidad
                tvtid = tvts[randint(0, len(tvts))]
                
                #------------------------------------------------------------##    
                #Ahora los historicos
                #Consulta historica, puede ser de cualquier parte de...
                delta       = (end_date-timedelta(minutes=arange))-start_date
                randomsecs  = randint(0, delta.seconds)
                afrom       = start_date + timedelta(seconds=randomsecs)
                ato         = afrom + timedelta(minutes=arange)
                print("Consulta efectiva: ->", afrom, ato, tvtid)
                
                TlmyVar._meta.db_table = "Telemetry_tlmyvar"
                query = """
                    SELECT *
                    FROM "Telemetry_tlmyvar" 
                    WHERE "Telemetry_tlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}' AND
                            "Telemetry_tlmyvar"."tlmyVarType_id" = {}
                    ORDER BY "Telemetry_tlmyvar".tstamp DESC;
                """.format(afrom, ato, tvtid)
                avars = TlmyVar.objects.raw(query)
                start = time.time()
                avars._fetch_all()
                end = time.time()
                normaltabletimeshist.append(end-start)
                
                print("Result set len: ", len(avars));
                
                
                
                TlmyVar._meta.db_table = "Telemetry_htlmyvar"
                query = """
                    SELECT *
                    FROM "Telemetry_htlmyvar" 
                    WHERE "Telemetry_htlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M:%S}' and '{:%Y-%m-%d %H:%M:%S}' AND
                            "Telemetry_htlmyvar"."tlmyVarType_id" = {}
                    ORDER BY "Telemetry_htlmyvar".tstamp DESC;
                """.format(afrom, ato, tvtid)
        
                avars = TlmyVar.objects.raw(query)
                start = time.time()
                avars._fetch_all()
                end = time.time()
                hipertablestimehist.append(end-start)
                
                print("Result set len(hist): ", len(avars));
                
                    
                
                
                #vuelvo original
                TlmyVar._meta.db_table = "Telemetry_tlmyvar"
            
            
            Log.create("SE-NORMTABLENN",      sum(normaltabletimes)/len(normaltabletimes) , str(cr), Log.INFORMATION).save()
            Log.create("SE-HIPERTABLENN",     sum(hipertabletimes)/len(hipertabletimes), str(cr), Log.INFORMATION).save()
            print("Medias seleccion tiempor real guardadas, ttcount=", cr);
            
            Log.create("SE-HISTNORMTABLENN",  sum(normaltabletimeshist)/len(normaltabletimeshist), str(cr), Log.INFORMATION).save()
            Log.create("SE-HISTHIPERTABLENN", sum(hipertablestimehist)/len(hipertablestimehist), str(cr), Log.INFORMATION).save()
            print("Medias seleccion historicas guardadas, ttcount=", cr);
        
        except Exception as ex:
            print(ex)
            time.sleep(10)