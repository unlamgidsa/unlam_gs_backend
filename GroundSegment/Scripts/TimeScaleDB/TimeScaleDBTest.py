'''
Created on 8 jun. 2020

@author: pablo
'''

#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDBTest.py

import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

def load(aid, tstamp):
    sats =  [Satellite.objects.get(code="BDSat1"), Satellite.objects.get(code="BDSat2"),  Satellite.objects.get(code="BDSat3")]
    aid = aid + 1
    tlvsl = []
    for sat in sats:
        
        tvts = sat.tmlyVarType.all()
        print("Generado para satelite", sat.code, len(tvts))
        afrom = tstamp #Fecha mas grande, asumo sincronizado todo!
        
        ato = afrom + timedelta(seconds=8)
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
            tvar.pk             = aid
            aid = aid + 1
            
            
            #raw+datetime
            #l_time = time.time()
            tvar.setValue(fcv, ato) 
            
            tvar.calIValue = fcv;
            tvar.calSValue = "";
            tvar.calFValue = fcv;
            tvar.calBValue = False;
            #tvar.calIValue = fcv;
            #l_ftime =  time.time()
            tlvsl.append(tvar)
            
    return tlvsl, aid
            #
            #print("totals:", g_ftime-g_time, l_ftime-l_time,  ((l_ftime-l_time)/(g_ftime-g_time))*100)

def periodspackets(period, tlvsl, last):
    
    #ultimo paquete
    TlmyVar._meta.db_table = "Telemetry_tlmyvar"
    pivot = last.tstamp+timedelta(seconds=8)
    final = pivot+timedelta(minutes=period) #mas corto para test!
    
    normaltimes = []
    hipertimes  = []
    aid = last.id + 1
    for tv in tlvsl:
        tv.tstamp   = pivot
        tv.id       = aid
        aid         = aid+1
        
    #bloques de dos horas
    while(pivot<final):
        
        TlmyVar._meta.db_table = "Telemetry_tlmyvar"
        start = time.time()
        TlmyVar.objects.bulk_create(tlvsl)   
        end = time.time()
        normaltimes.append(end-start)
        
        
        TlmyVar._meta.db_table = "Telemetry_htlmyvar"
        start = time.time()
        TlmyVar.objects.bulk_create(tlvsl)   
        end = time.time()
        hipertimes.append(end-start)
               
               
        pivot=pivot+timedelta(seconds=8)
        
        for tv in tlvsl:
            tv.tstamp   = pivot
            tv.id       = aid
            aid         = aid+1
            
        print("Periodo ", pivot)
        print("Restan...", (final-pivot).total_seconds());
    
    print("Guardando medias de insercion")
    ttcount = TlmyVar.objects.count()
    Log.create("TI-NORMTABLE", sum(normaltimes)/len(normaltimes) , str(ttcount), Log.INFORMATION).save()
    Log.create("TI-HIPERTABLE", sum(hipertimes)/len(hipertimes), str(ttcount), Log.INFORMATION).save()
        

    
    

if __name__ == '__main__':
    sats =  [Satellite.objects.get(code="BDSat1").code, Satellite.objects.get(code="BDSat2").code,  Satellite.objects.get(code="BDSat3").code]
    tvts = TlmyVarType.objects.filter(satellite__code__in = sats).values_list('pk', flat=True)
    #Log.objects.all().delete()
    
    tlvsl = []
    #5*6=media hora
    for i in range(36):
        #una hora de paquetes antes de los test de velocidad
        print("Por ingresar nuevo bloque datos")
        last = TlmyVar.objects.order_by().order_by('id').last()
        if(len(tlvsl)==0):
            tlvsl, aid = load(last.id, last.tstamp);
        periodspackets(5, tlvsl, last)
        
        print("Bloque de datos ingresados!")
        TlmyVar._meta.db_table = "Telemetry_tlmyvar"
        start_date  = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).first().tstamp
        end_date    = TlmyVar.objects.filter(tlmyVarType__satellite__code__in=sats).last().tstamp
        
        normaltabletimes = []
        hipertabletimes = []
        normaltabletimeshist = []
        hipertablestimehist = []
        #100 consultas para test de velovidad
        j = 0
        while(j<100):
        #for w in range(100):
            #90% ultima hora 10% historicas con tiempos aleatorios entre 3 y 15 minutos
            range    = randint(3,15)
            tvtid = tvts[randint(0, len(tvts))]
        
            #consultas tiempo real
            afrom    = end_date-timedelta(minutes=range)
            ato      = end_date; 
            
            query = """
                SELECT *
                FROM "Telemetry_tlmyvar" 
                WHERE "Telemetry_tlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                        "Telemetry_tlmyvar"."tlmyVarType_id" = {}
                ORDER BY "Telemetry_tlmyvar".tstamp DESC;
            """.format(afrom, ato, tvtid)
            avars = TlmyVar.objects.raw(query)
            start = time.time()
            avars._fetch_all()
            end = time.time()
            normaltabletimes.append(end-start)
            
            if len(avars)==0:
                print("Erro no deberia pasar jamas");
            
            
            
            TlmyVar._meta.db_table = "Telemetry_htlmyvar"
            query = """
                SELECT *
                FROM "Telemetry_htlmyvar" 
                WHERE "Telemetry_htlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                        "Telemetry_htlmyvar"."tlmyVarType_id" = {}
                ORDER BY "Telemetry_htlmyvar".tstamp DESC;
            """.format(afrom, ato, tvtid)
    
            avars = TlmyVar.objects.raw(query)
            start = time.time()
            avars._fetch_all()
            end = time.time()
            hipertabletimes.append(end-start)
            
            j = j + 1;
            if len(avars)==0:
                print("Erro no deberia pasar jamas");
                
                
                
            #Ahora los historicos
            #Consulta historica, puede ser de cualquier parte de...
            delta       = (end_date-timedelta(minutes=range))-start_date
            randomsecs  = randint(0, delta.seconds)
            afrom       = start_date + timedelta(seconds=randomsecs)
            ato         = afrom + timedelta(minutes=range)
            TlmyVar._meta.db_table = "Telemetry_tlmyvar"
            query = """
                SELECT *
                FROM "Telemetry_tlmyvar" 
                WHERE "Telemetry_tlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                        "Telemetry_tlmyvar"."tlmyVarType_id" = {}
                ORDER BY "Telemetry_tlmyvar".tstamp DESC;
            """.format(afrom, ato, tvtid)
            avars = TlmyVar.objects.raw(query)
            start = time.time()
            avars._fetch_all()
            end = time.time()
            normaltabletimeshist.append(end-start)
            
            if len(avars)==0:
                print("Erro no deberia pasar jamas");
            
            
            
            TlmyVar._meta.db_table = "Telemetry_htlmyvar"
            query = """
                SELECT *
                FROM "Telemetry_htlmyvar" 
                WHERE "Telemetry_htlmyvar"."tstamp" BETWEEN '{:%Y-%m-%d %H:%M}' and '{:%Y-%m-%d %H:%M}' AND
                        "Telemetry_htlmyvar"."tlmyVarType_id" = {}
                ORDER BY "Telemetry_htlmyvar".tstamp DESC;
            """.format(afrom, ato, tvtid)
    
            avars = TlmyVar.objects.raw(query)
            start = time.time()
            avars._fetch_all()
            end = time.time()
            hipertablestimehist.append(end-start)
            j = j + 1;
            if len(avars)==0:
                print("Erro no deberia pasar jamas");
            
            
            #vuelvo original
            TlmyVar._meta.db_table = "Telemetry_tlmyvar"
            
        
        cr = TlmyVar.objects.count();
        Log.create("SE-NORMTABLE",      sum(normaltabletimes)/len(normaltabletimes) , str(cr), Log.INFORMATION).save()
        Log.create("SE-HIPERTABLE",     sum(hipertabletimes)/len(hipertabletimes), str(cr), Log.INFORMATION).save()
        Log.create("SE-HISTNORMTABLE",  sum(normaltabletimeshist)/len(normaltabletimeshist), str(cr), Log.INFORMATION).save()
        Log.create("SE-HISTHIPERTABLE", sum(hipertablestimehist)/len(hipertablestimehist), str(cr), Log.INFORMATION).save()
        
    print("Fin de programa")
    

    """
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    """
     

    