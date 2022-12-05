'''
Created on 25 de nov. de 2016

@author: pabli
'''

import os, sys

#sys.path.append('C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment')
sys.path.append('/home/ubuntumate/git/GroundSegment/GroundSegment/')

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet
from django.db import transaction
import threading
import time
from django.db import connection
import psycopg2


def SaveTlmyUpdates(dirtyObject, n):
    print("Salvando actualizaciones de telemetria, esto es thread safe?")
    t0 = time.time()
    for o in dirtyObject.values():
        o.save()
    t1 = time.time()    
        
    print("Se finaliza la actualizacion de telemetria n: ", n, " en ", t1-t0, " segundos.")

def RawSaveTlmyUpdates(dirtyObject, n):
    print("Salvando actualizaciones de telemetria, esto es thread safe?")
    t0 = time.time()
    

    try:
        conn = psycopg2.connect("dbname='DBGroundSegment' user='gs' host='127.0.0.1' password='gs'")
    except:
        print ("I am unable to connect to the database")
    #'UPDATE "GroundSegment_tlmyvartype" SET "lastCalFValue" = %s WHERE id = %s', [o.getValue(), o.pk]
    cur = conn.cursor()
    
    fs = ""
    for o in dirtyObject.values():
        fs = fs + 'UPDATE "GroundSegment_tlmyvartype" SET "lastCalFValue" = '+str(o.getValue()) + ' WHERE id = ' +str(o.pk) +";"
        
    cur.execute(fs)
    t1 = time.time()    
        
    print("Se finaliza la actualizacion de telemetria n: ", n, " en ", t1-t0, " segundos.")

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

from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TmlyVar import TlmyVar


def SaveTlmy(dirtyObjects, n):
    t0 = time.time()
    TlmyVar.objects.bulk_create(dirtyObjects)
    t1 = time.time()
    print("Salvado, objectos: ", len(dirtyObjects), " tiempo: ",(t1-t0)*1000, " ms")        


if __name__ == '__main__':
    
  
    #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #proj_path = "/home/ubuntumate/git/GroundSegment/GroundSegment"
            
    
    """
    Primero que nada creamos 100.000 variables de telemetria si aun no existen
    
    """
    cant = TlmyVarType.objects.all().count()
    createcount = 100000-cant
    sat = Satellite.objects.get(code="FS2017")
    
    

    afrom = cant
    tlmVarTypeList = []
    ra = rn.Random()
    
    print("Generando variables de telemetria..")
    for i in range(afrom, createcount):
        print("Generando..", i)
    
        tm = TlmyVarType()
        tm.satellite = sat
        tm.code = "VS"+str(i)
        tm.description = "Variable simulada n "+str(i)
        tm.limitMaxValue = ra.randrange(50.0, 100.0)
        tm.limitMinValue = ra.randrange(0.0, 49.0)
        
        tm.maxValue = tm.limitMaxValue
        tm.minValue = tm.limitMinValue
        
        
        
        tm.varType = tm.FLOAT
        tm.varSubType = tm.DERIVED
        if i<10000:
            tm.varSubType = tm.DIRECT
        
        #A una de cuatro le asigno una funcion de calibracion
        if rn.randrange(1, 4)==2:
            tm.calibrationMethod = Calibration.objects.all().order_by('?').first()
        
        tm.setValue(ra.randrange(tm.minValue, tm.maxValue))
        
        tlmVarTypeList.append(tm)
        
            
        #tm.save()
    
      
    
    if len(tlmVarTypeList)>0:
        
        print("100.000 tipos de variables generadas, listo para guardar")
        t0 = time.time()
        TlmyVarType.objects.bulk_create(tlmVarTypeList)
        t1 = time.time()
        print("Variables almacenadas, tiempo de guardado...{:.2f}".format(t1-t0))
        
    
    #Supongo que por frame de telemetria me pueden llegar 500 variables,
    #selecciono 500 al azar
    print("Generando elementos de simulacion")
    allTlmyVar = TlmyVarType.objects.filter(satellite=sat).filter(varSubType=TlmyVarType.DIRECT)
    
    tlmySimulator = {}
    for x in range(500):
        tm = allTlmyVar.order_by('?').first()
        #La mayoria de las veces la telemetria no cambia
        if rn.randrange(0,5)==3:
            tlmySimulator[tm.pk] = tm.getValue()+rn.randrange(0,1)
            if tlmySimulator[tm.pk]>tm.limitMaxValue:
                tlmySimulator[tm.pk]=tm.limitMaxValue
    
    
    dAllTlmyVar = {}
    for t in allTlmyVar:
        dAllTlmyVar[t.pk] = t
        
    print("Elementos de simulacion generados")
    
    threads = list()
    simCant = int( input("Indique cantidad de simulaciones...") )
    
    n = 0
    for sc in range(simCant):
        dirtyObjects = []  
        tstart = time.time()
        
        for k, v in tlmySimulator.items():
            tel = dAllTlmyVar[k]       
            dirtyObjects.append( tel.setValue(v, True) )
        
          
        tend = time.time()
        #TlmyVar.objects.bulk_create(dirtyObjects)
        #tendwsave = time.time()
        print("Actualizacion de variables, tiempo ", (tend-tstart)*1000, " ms")
        #print("Simulacion actualizacion de variables con persistancia demora ", (tendwsave-tstart)*1000, " millisegundos")
        
        
        n=n+1
        t = threading.Thread(target=SaveTlmy(dirtyObjects, n))
        threads.append(t)
        t.start()
        
    

    
  
    