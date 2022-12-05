'''
Created on 25 jun. 2018

@author: pablo
'''

# Create your tasks here
from __future__ import absolute_import, unicode_literals
import os, sys, glob 
from struct import unpack

#from celery import task, shared_task
#from celery import Task
#from celery.utils.log import get_task_logger
#from celery._state import current_app


from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from Telemetry.models.TlmyVar import TlmyVar
from fileinput import close
from datetime import datetime, timedelta
import requests
import json
from rest_framework import status
from struct import unpack
import binascii
from GroundSegment.Utils.Console import Console, NORMAL, WARNING, ERROR
from GroundSegment.Utils.Utils import loadOrCreateParam
import socket
from django.utils import timezone
import multiprocessing as mp
import gzip
from http import HTTPStatus

import re
import time

import dateutil.parser
from _datetime import tzinfo
import pytz
from Telemetry.models.FrameType import FrameType
from Telemetry.models.TlmyVar import TlmyVar

from django.core.exceptions import ObjectDoesNotExist
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from django.utils.timezone import utc
from django.db import reset_queries
from django.db import connection




#logger = get_task_logger("telemetry")


"""
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyRawData import TlmyRawData
lit = Satellite.objects.get(code="LITUANICASAT2")
TlmyRawData.objects.filter(source="LITUANICASAT2").delete()
TlmyRawData.objects.filter(source="LITUANICASAT2", state=TlmyRawData.PROCESSED).update(state=TlmyRawData.PENDING)
TlmyVar.objects.filter(tlmyVarType__satellite=lit).delete()

import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.BLTlmyVar import BLTlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType

#TlmyRawData.objects.filter(source="SACD", state=TlmyRawData.PROCESSED).update(state=TlmyRawData.PENDING)
Alternativa 1
--------------
BLTlmyVar.objects.all().delete()
TlmyRawData.objects.filter(source="SACD").delete()
TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").delete()

Alternativa 2
--------------
BLTlmyVar.objects.all().delete()
TlmyRawData.objects.filter(source="SACD").delete()
tlmt = TlmyVarType.objects.filter(satellite__code="SACD")
tlmids=TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").values_list('id', flat=True)[0:500000]
while(len(tlmids)>0):
    TlmyVar.objects.filter(pk__in=tlmids).delete()
    tlmids=TlmyVar.objects.filter(tlmyVarType__satellite__code="SACD").values_list('id', flat=True)[0:500000]
    print("Bloque borrado")
    


. env/bin/activate
"""

from django.core.cache import cache
from contextlib import contextmanager
from Utils.PktsHelpers import ExtractFS2017AX25Payload, sendJsonDataPkt, DireWolfFile
#from .signals import announce_new_tlmy


#from celery import current_app
from GroundSegment.settings import APIURL

from Calibration import *
from django.db.models import Q

#antigua version con Celery
#class TlmyDecode(current_app.Task):


def is_set(x, n):
    return x[n//8] & 2**(n//8) != 0
class TlmyDecode():
    name = 'tasks.tlmyDecode'
    _tvts = {}   
    
    _satellite = None
    
    def __init__(self):
        self._tvts = {}
        self._satellites = {}
        super().__init__() 
        
    def run(self, pk, etvts): 
        #etvts tipos de variables externos, para dejar logica unica 
        #cuando se procesa un raw entero que cuando solo se requiere 
        #regenerar variables 
        
        result = ""
        
        tlmyRawData = TlmyRawData.objects.get(pk=pk)
        rd = tlmyRawData
        payload = rd.getPayloadBlob()
        raw = rd.getBlob()
        
        
        

        satellite = tlmyRawData.satellite
        if satellite.code in self._satellites:
            #sobreescribo con el objeto que tiene la funcion de extracion 
            #previamente cargada
            satellite = self._satellites[satellite.code]
        else:
            self._satellites[satellite.code] = satellite
        
        frameType = None
        #Consulto si la logica necesaria para extraer el tipo de fram
        #ya esta cargada
        if satellite.extractFrameTypeFun!=None:
            if not satellite.extractFrameTypeLogic:
                #Cargar via reflexion
                klass = globals()[satellite.extractFrameTypeFun.aClass]
                instance = klass()
                methodToCall = getattr(instance, satellite.extractFrameTypeFun.aMethod)
                satellite.extractFrameTypeLogic = methodToCall
            else:
                pass
                
            try:
                frameType = FrameType.objects.get(aid=satellite.extractFrameTypeLogic(None, raw))
            except ObjectDoesNotExist:
                frameType = None
               
        #ponerle vencimiento a las listas de tipos de variables de telemetria
        ft = -1
        if frameType!=None:
            ft = frameType.aid
            tlmyRawData.frameType = frameType
            #tlmyRawData.save()
        else:
            pass
        
        if (tlmyRawData.satellite.code, ft) in self._tvts:
            #print("Tipos de variables de telemetria cacheados")
            
            pass
        else:
            print("A cachear")
            #meto en cache con par satellite+tipo de frame
            if etvts==None:
                #no hay tipo de frame, no se acepta, no es reconocido
                self._tvts[tlmyRawData.satellite.code, ft] = tlmyRawData.satellite.tmlyVarType.filter(Q(frameType__aid=ft) or Q(ft=0)) 
                print("y se cachea ", tlmyRawData.satellite.code, ft, self._tvts[tlmyRawData.satellite.code, ft])
            
            else:
                #De las variables externas pasadas como parametros tambien requieren filtrar por tipo de frame
                self._tvts[tlmyRawData.satellite.code, ft] = etvts.filter(Q(frameType__aid=ft))
                print("no se", ft, self._tvts[tlmyRawData.satellite.code, ft])
                
        
        #recupero del cache, tiene que tener frame type
        tvts = self._tvts[tlmyRawData.satellite.code, ft] 
        print("Tenemos los tipos del cache", len(tvts))
        arranque = time.time()
        tlvsl = []
        #las variables en tvts son unicamente las que se corresponden con el tipo de frame
        for tt in tvts:
            try:
                if (tt.varSubType==1):
                    #Telemetria derivada
                    raw = rd.id
                else:
                    if tt.bitsLen >= 8:
                        raw = payload[tt.position:tt.position+tt.ctype.length]
                    elif tt.bitsLen == 1:
                        raw = is_set(payload[tt.position], tt.subPosition)
                    else:
                        #Not implemented yet
                        pass
                    
                
                tvar                = TlmyVar()
                tvar.code           = tt.code
                tvar.tlmyVarType    = tt
                tvar.tlmyRawData    = rd
                tvar.setValue(raw, rd.pktdatetime)
                
                tlvsl.append(tvar)
                
                #tvar.save()
                
    
                #se da aviso de que la variable ha sido actualizada
                
            except Exception as ex:
                #Errores al procesar la data, tipicamente el registro no tiene la cantidad de
                #bytes, el raw esta corrupto
                rd.state            = TlmyRawData.ABORTED
                
                rd.abortedError     = "Exception in tlmy "+tt.code+" "+ex.__str__()
                rd.save()
                result = result + "Exception: ({0}): {1}".format(type(ex), ex.__str__())
           
        print("El proceso se comio : {:.2f}".format(time.time()-arranque))        
        #print("Total bucle", (datetime.now()-stt).total_seconds(), "segundos")    
        
        #Si por el contrario esta en aborted quiere decir que hubo falla, no lo toco.
        if(rd.state==TlmyRawData.PENDING):
            rd.state            = TlmyRawData.PROCESSED
            rd.save()
        
        try:  
            #stt = datetime.now();
            #TODO: Revisar la actualizacion de tipos, no tiene sentido si la interfaz de tiempo real
            #van a ser websockets de tiempo real
            #ss = time.time()
            #TlmyVarType.objects.updateTlmyType(tvtypsList, updateFieldList)
            #print("Tiempo actualizacion de tipos", time.time()-ss, "Cantidad de elementos: ", len(tvtypsList))
            #print("Se salvan:", len(tlvsl))
            #Fin de actualizacion de tipos
            
            ss = time.time()
            TlmyVar.objects.bulk_create(tlvsl)
            #for v in tlvsl:
            #    v.save()      
            print("Tiempo guardado de vars {:.2f}".format(time.time()-ss))
            #TODO: recuperar bulk create meter algun patrón para resolver el problema
            #TlmyVar.objects.bulk_create(tlvsl)
            #print("Bulk->", (datetime.now()-stt).total_seconds(), "segundos")
        except Exception as ex:
            result = result + "Exception: ({0}): {1}".format(type(ex), ex.__str__())
            print(result)
            
        
        return result
    
"""
tlmyDecode = TlmyDecode()
current_app.tasks.register(tlmyDecode)
tlmyDecode.delay()
"""
     #implementar :
    #on_failure(self, exc, task_id, args, kwargs, einfo)
    #on_retry(self, exc, task_id, args, kwargs, einfo)
    #on_success(self, retval, task_id, args, kwargs)


                
 


"""
@app.task(base=TlmyDecode)
def tlmyDecode(self, pk):
    terminar esto!
    self.delay(pk)
"""    
  

#@app.task(bind=True)
def TitaAdapter(self):
    """
    Se conecta con puerto direwolf comando:
    direwolf -B 9600 -b 16 -n 1 -r 48000 -t 0 -d p -d t
    Lee paquetes por interfaz TCP ip KISS y los inserta
    
    #esta linea muestra los resultados en hexa.
    direwolf -t 0 -p -B 9600 -b 16 -n 1 -r 48000 -q h -q d -d p -d t - < file.raw
    
    Por archivos
    direwolf -t 0 -p -B 9600 -b 16 -n 1 -r 48000 -q -p - < archivo.wav
    
    
    sox -t wav CSIM_20210430_135313_437259413.wav -esigned-integer -b16 -r 22050 -t raw CSIM.raw
    
    //la decodificacion parece exitosa con archivos bajados de satnogs
    multimon-ng -t raw -a FSK9600 CSIM_SatNogs.raw
    
        
    
    
    """
    sat     = Satellite.objects.get(code="TITA")
    
    while True:
        uhfServerIp             = loadOrCreateParam("UHF_TITA_SERVER_IP", "GroundStation", "127.0.0.1", "IP del servidor TCP TITA de la antena UHF")
        uhfServerPort           = loadOrCreateParam("UHF_TITA_SERVER_PORT", "GroundStation", "8001", "Puerto del servidor TCP TITA de la antena UHF")    
            
            
        BUFFER_SIZE             = loadOrCreateParam("UHF_BUFFER_SIZE", "GroundStation", "1024", "Tamanio del buffer del cliente TCP")
        DISCONNECTION_SLEEP     = loadOrCreateParam("UHF_DISCONNECTION_SLEEP", "GroundStation", "10", "Tiempo en que se duerme la aplicacion ante una desconexion a la espera de volver a intentar")
        
        Console.log("Done..trying to connect ip "+uhfServerIp+" ,port "+uhfServerPort)
        
        unconnectionLimit       = 0
        i = 0
        while unconnectionLimit<10:
            
            Console.log("Create o recreate socket...", str(datetime.utcnow()))
            
            """
            Creo el socket -Cliente- que se conectara al software de la antena
            """            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                socket.setdefaulttimeout(5.0)
                s.connect( (sat.commServerIP, int(sat.commServerPort)) )
                
                try:
                    Console.log("Successfully connection to.."+uhfServerPort)
                    while True:
                        try:
                            """
                            Establezco un timeout para la bajada, con o sin bajada los comandos deben ser enviados
                            """
                            s.settimeout(5.0)
                            
                            """
                            Me quedo esperando recibir informacion del socket (IPC)
                            """    
                            chunk = s.recv(int(BUFFER_SIZE))
                            unconnectionLimit = 0
                            """
                            Si recibo telemetria, defenitivamente estoy en contacto
                            """
                            sat.setInContact(True)
                            
                            """
                            Si la informacion es una trama de bits completa la proceso
                            """
                            if chunk == b'':
                                #print("Socket connection broken")
                                raise RuntimeError("socket connection broken")
                            else:
                                """
                                Me guardo el crudo tal cual llego antes de procesarlo, la tabla donde se guarda es TlmyRawData
                                """
                                #os.system('cls||clear')
                                Console.log("--------------------Data Received-------------------")
                                print("\nData Received("+str(timezone.datetime.utcnow() )+")\nData->", chunk)
                                
                                payload = chunk.hex()
                                #Descarto los dos primeros bytes, no sabemos que es
                                SendTitaPacket(datetime.utcnow(), "REALTIME", payload[4:-1].upper(), True)
                                
                        except Exception as err:
                            Console.log(err.__str__(), WARNING) 
                        
                except Exception as err:
                    Console.log(err.__str__(), WARNING) 
            
            except Exception as err:
                Console.log(err.__str__(), WARNING) 
                
def SendTitaPacket(dt, tag, payload, realtime):
    
    jdata = {}
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    index = payload.find('FFFFF00001')
    if index==-1:
        print("Unknown packet")
        return
    
    fpayload = payload[index:-1]
    
    
    #el = re.search("fffff00001", payload, re.IGNORECASE)
    #fpayload = payload[el.start(): -1]
    
    if len(fpayload)%2!=0:
        fpayload = fpayload[0:-2]
        
    #En la posicion nueve esta el unixdatetime
    try:
        raw = binascii.unhexlify(fpayload[(9*2):(9*2)+(4*2)])
        raw = unpack('>I', raw)[0]
        basedate = datetime(1970,1,1)
        delta = timedelta(seconds=raw)
        pktdt = basedate+delta
    except Exception as err:
        Console.log(err.__str__(), ERROR) 
        pktdt = dt
    
    
    jdata['capturedAt']     = dt.isoformat()
    jdata['pktdatetime']    = pktdt.isoformat()#dt.isoformat()#pktdt.isoformat()#pktdt.isoformat()
    jdata['source']         = "TITA"
    jdata['strdata']        = fpayload
    jdata['realTime']       = realtime
    jdata['tag']            = tag
    #jdata['strpayload']     = fpayload
    jsondata                = json.dumps(jdata)
    
    res = requests.post(url=APIURL, headers=headers, data=jsondata)
            
    if res.status_code!=status.HTTP_201_CREATED:
        #logger.info(res.json()["errors"])
        print(res.status_code, res.reason)    
    
    
def sendSACDChunk(chunk):
    try:
        dtn = datetime.utcnow()
        #La fecha hora del packet la debo extraer del CDH Time...
        secs = unpack('>I', chunk[100:104])[0] 
        basedate = datetime(1980,1,6)
        pktdt = basedate+timedelta(seconds=secs)
    
        #las tramas son de 4000 bytes, que tal si leemos asi?
        sendJsonDataPkt(APIURL, dtn , pktdt, "SACD", chunk.hex(), chunk.hex(), False, "FILE")
        #SendSACDPacket(pktdt, "FROMFILE", strm.hex(), False)
    except Exception as ex:
        print("Error Sending SACDCHUNK", ex)




#@app.task(bind=True)
def SACDFileAdapter(self):
    FRAMELEN = 4000
        
    print("Corriendo SACD File Adapter(Distribuido)")
    pathBase = os.path.dirname(os.path.abspath(__file__))
       
    print("Buscando archivos SACD...", pathBase+"/PendingTlmy/SAC-D/*.gz")
    
    
    #Muevo todo a carpeta de procesado, para evitar problemas de concurrencia
    filestoproc = []
    for file in glob.glob(pathBase+"/PendingTlmy/SAC-D/*.gz"):
        path, filename = os.path.split(file)
        pfile = pathBase+"/ProcessedTlmy/SAC-D/"+filename
        os.rename(file, pfile)
        filestoproc.append(pfile)
    
    for pfile in filestoproc:   
        path, filename = os.path.split(pfile)
        cf = gzip.open(pfile, 'rb')
        
        try:
            #sttick  = time.process_time()
            start  = time.time()
            pkts = 1
            strm = cf.read(FRAMELEN)
            while(len(strm)==FRAMELEN):
                sendSACDChunk(strm)
                strm = cf.read(FRAMELEN)
                pkts = pkts + 1
                
            #entick = time.process_time()
            end  = time.time()
            
            
            print("Paquete SAC-D finalizado total chunks", pkts, " Tiempo en segundos", end-start)
            
            cf.close()
        
        
            #mover
            print("-------------------------------")
            
            print("Finalizado archivo SACD", filename)
        except Exception as ex:
            print("Error in file", ex)
            path, filename = os.path.split(pfile)
            os.rename(pfile, pathBase+"/ErrorFiles/SAC-D/"+filename)
            cf.close()
    
            
    print("Fin de recorrida de archivos SACD")


  


def SACDFileAdapterParallel(self):
    FRAMELEN = 4000
    max_apply_size = 100
    cpucount = mp.cpu_count()
    
    pool = mp.Pool(processes=cpucount)
    
    
    print("Corriendo SACD File Adapter")
    pathBase = os.path.dirname(os.path.abspath(__file__))
       
    print("Buscando archivos SACD...", pathBase+"/PendingTlmy/SAC-D/*.gz")
    for file in glob.glob(pathBase+"/PendingTlmy/SAC-D/*.gz"):
        #Abro archivo comprimido
        #file = "/home/psoligo/git/GroundSegment/GroundSegment/Telemetry/PendingTlmy/SAC-D/CGSS_20150605_221100_10020150605215102_SACD_HKTMST.bin.gz"
        cf = gzip.open(file, 'rb')
        
        try:
            #sttick  = time.process_time()
            start  = time.time()
            pkts = 1
            strm = cf.read(FRAMELEN)
            while(len(strm)==FRAMELEN):
                pool.apply_async(sendSACDChunk, args=(strm,))
                #sendSACDChunk(strm)
                strm = cf.read(FRAMELEN)
                pkts = pkts + 1
                #if (pkts%100)==0:
                #    print("Pool Size:", pool._taskqueue.qsize())
                while pool._taskqueue.qsize() > max_apply_size:
                    time.sleep(1)
            
            #entick = time.process_time()
            end  = time.time()
            
            
            print("Paquete SAC-D finalizado total chunks", pkts, " Tiempo en segundos", end-start)
            
            cf.close()
        
        
            #mover
            print("-------------------------------")
            path, filename = os.path.split(file)
            os.rename(file, pathBase+"/ProcessedTlmy/SAC-D/"+filename)
            print("Finalizado archivo SACD", filename)
        except Exception as ex:
            print("Error in file", ex)
            path, filename = os.path.split(file)
            os.rename(file, pathBase+"/ErrorFiles/SAC-D/"+filename)
            cf.close()
    
    pool.close();
    pool.join();        
            
    print("Fin de recorrida de archivos SACD")
 
#@app.task(bind=True)
def FS2017DBAdapter(self):
    
    fs2017 = Satellite.objects.get(code="FS2017")
    print("Se eliminan ", fs2017.rawdatas.count(), " registros")
    fs2017.rawdatas.all().delete()
    
    
    import psycopg2
    conn = psycopg2.connect("dbname=DBGS user=postgres password=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    cur.execute("""select * from "FS2017_uhfrawdata" where upper(source)!=upper('simulation') and length(data)>80 """)
    cant = cur.rowcount
    cont = 0
    row = cur.fetchone()
    while row is not None:
        if cont%50 == 0:
            print("Se procesaron", cont, "de", cant)
        cont = cont + 1
        
        pktdt = datetime.utcnow()
        data = row["data"].tobytes()
        payload = ExtractFS2017AX25Payload(data)
        if payload!=None:
            sendJsonDataPkt(APIURL, row['created'], row['created'], "FS2017", row["data"].hex(), payload.hex(), False, "Database")
        row = cur.fetchone()
        
    cur.close()
    conn.close();
    
        
        

    