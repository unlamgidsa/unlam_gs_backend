'''
Created on 23-jul-2021

@author: pabli
'''
import gzip
import os, sys, glob 
import time
from struct import unpack
from datetime import datetime, timedelta
from Scripts.DSUtils import getProjectPath
import pytz



BASE_DIR = getProjectPath()
os.chdir(BASE_DIR)

import sys; 
print('%s %s' % (sys.executable or sys.platform, sys.version))
os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from Telemetry.models.TlmyRawData import TlmyRawData
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.FrameType import FrameType
if __name__ == '__main__':

    sat = Satellite.objects.get(code="SAC-D") 
    ft = FrameType.objects.get(aid=4000)  
    
    #TlmyRawData.objects.filter(satellite=sat).delete() 
    FRAMELEN = 4000
    print("Corriendo SACD File Adapter")
    path = "C:\\Users\\pabli\\OneDrive - Universidad Nacional de la Matanza\\UNLAM\\Investigacion\\C211\\Data\\Telemetria\\SACD\\*.gz"
    print("Buscando archivos SACD...")
    for file in glob.glob(path):
        #Abro archivo comprimido
        #file = "/home/psoligo/git/GroundSegment/GroundSegment/Telemetry/PendingTlmy/SAC-D/CGSS_20150605_221100_10020150605215102_SACD_HKTMST.bin.gz"
        cf = gzip.open(file, 'rb')
        try:
            #sttick  = time.process_time()
            start  = time.time()
            pkts = 1
            strm = cf.read(FRAMELEN)
            while(len(strm)==FRAMELEN):
                
                try:
                  dtn = datetime.utcnow().replace(tzinfo=pytz.UTC)
                  #dtn = dtn.replace(tzinfo=pytz.UTC) 
                  #La fecha hora del packet la debo extraer del CDH Time...
                  secs = unpack('>I', strm[100:104])[0] 
                  basedate = datetime(1980,1,6, tzinfo=pytz.UTC)
                  pktdt = basedate+timedelta(seconds=secs)
                  #print(pktdt)
                  rd = TlmyRawData(created=dtn,
                                   capturedAt=dtn,
                                   pktdatetime=pktdt,
                                   data=strm,
                                   pylStart=0,
                                   pylEnd=len(strm),
                                   source="Direct",
                                   state=0,
                                   realTime=False, 
                                   tag="Direct",
                                   satellite=sat,
                                   frameType=ft)
                  rd.save()
                  
   
                  
                  #las tramas son de 4000 bytes, que tal si leemos asi?
                  #sendJsonDataPkt(APIURL, dtn , pktdt, "SACD", chunk.hex(), chunk.hex(), False, "FILE")
                  #SendSACDPacket(pktdt, "FROMFILE", strm.hex(), False)
                except Exception as ex:
                  pass
                  #print("Error Sending SACDCHUNK", ex)
                
                strm = cf.read(FRAMELEN)
                pkts = pkts + 1

            
            #entick = time.process_time()
            end  = time.time()
            
            
            print("Paquete SAC-D finalizado total chunks", pkts, " Tiempo en segundos", end-start)
            #mover
            print("-------------------------------")
            path, filename = os.path.split(file)
            #os.rename(file, pathBase+"/ProcessedTlmy/SAC-D/"+filename)
            print("Finalizado archivo SACD", filename)
            cf.close()
        except Exception as ex:
            print("Error in file", ex)
            cf.close()
            #path, filename = os.path.split(file)
            
            #os.rename(file, pathBase+"/ErrorFiles/SAC-D/"+filename)
            
    
            
    print("Fin de recorrida de archivos SACD")
