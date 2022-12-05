'''
Created on 28 mar. 2019

@author: psoligo
'''


from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta
import requests
import os
from celery import Celery
from Utils.PktsHelpers import sendJsonDataPkt
from GroundSegment.settings import APIURL
from django.utils.timezone import utc
#from celery.five import monotonic
#from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache
import argparse

import pytz
from rest_framework import status



# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroundSegment.settings')



#app = Celery('GroundSegment')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#app.config_from_object('django.conf:settings', namespace='CELERY')
#app.config_from_object('django.conf:settings', namespace='CELERY')
#app.conf.broker_url = 'redis://127.0.0.1:6379/0'
# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()

LOCK_EXPIRE = 60 * 10 * 24 #Tiene 24 horas para importar 

#logger = get_task_logger(__name__)

def loadDjangoApp():
    import sys; print('%s %s' % (sys.executable or sys.platform, sys.version))
    import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
    from django.core.wsgi import get_wsgi_application
    from attr._compat import isclass
    return get_wsgi_application()


"""
@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)
"""

#@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
class MaxSizeList(list):
    def __init__(self, maxlen):
        self._maxlen = maxlen

    def append(self, element):
        self.__delitem__(slice(0, len(self) == self._maxlen))
        super(MaxSizeList, self).append(element)



def rawInBd(sendsession, apiurl, sat, dtn):
  base_url_travailable = apiurl.replace("/TlmyRawData/", "/API/TlmyRawData/")+str(sat)+"/"+str(int(dtn.timestamp()))
  try:
    resp = sendsession.get(base_url_travailable)
    
    if(resp.json()=="{'detail': 'Authentication credentials were not provided.'}"):
      print("Error credenciales para autenticacion no provistas")
      return False
    else:
      return len(resp.json())>0;
    #paquete ya existente en la bd
  except Exception as ex:
    print(ex)
    #No existe paquete, hago get e inserto                              
    #sendsession.get(APIURL, sat, dt)
    return False
    
    #rg.content rg.text
def extractSatnogsURLDateTime(dd):
  dt = None
  try:
    try:
      dt = datetime.strptime(dd['payload_demod'][-19:], "%Y-%m-%dT%H-%M-%S").replace(tzinfo=pytz.UTC)
    except:
      try:
        dt = datetime.strptime(dd['payload_demod'][-21:-2], "%Y-%m-%dT%H-%M-%S").replace(tzinfo=pytz.UTC)
      except:
        dt = datetime.strptime(dd['payload_demod'][-22:-3], "%Y-%m-%dT%H-%M-%S").replace(tzinfo=pytz.UTC)
    
    return dt
  except Exception as ex:
    print("Error parsing de fecha satnogs en archivo ", ex)
    return None    
                
#@app.task(bind=True)
def TaskSATNOGSAdapter(self):
    #TlmyVar.objects.filter(tlmyVarType__satellite__code="TITA", tstamp__gte='2020-01-01').delete() //.
    #Satellite.objects.get(code="TITA").rawdatas.filter(pktdatetime__gte='2020-01-01').delete()
    """
    --apiurl "http://10.10.203.4:8001/TlmyRawData/"
    --user usuario
    --password passcorrespondiente
    --sats 40014 43793
    --days 3    
    """
    
    
    #sobreescribo api
    #TODO: Modificar para que celery soporte la parametrizacion
    
    parser = argparse.ArgumentParser(description='Interfaz satnogs')
    parser.add_argument("-a", "--apiurl", help="apiurl", type=str,required=True)
    parser.add_argument("-u", "--user", help="user", type=str,required=True)
    parser.add_argument("-p", "--password", help="password", type=str,required=True)
    parser.add_argument("-s", "--sats", type=int, nargs='+', help="satellite list norad ids", required=True)
    parser.add_argument("-d", "--days", type=int, help="days before", required=True)
    parser.add_argument("-v", "--verify", type=int, help="verify get", required=False, default=1)
    
    
    
    
    args = parser.parse_args()
    
    APIURL = args.apiurl
    #APIURL = "http://127.0.0.1:8001/TlmyRawData/"
    #86A2404040406098AA6E828200E103F0FFFFF00001000043635BE433950006DE840828CD98010100006A480201000000006F030100002D85035B0017034401C90369009804010DA50415050100000000D4C0F9CA2EC304AFFFA8006CFFF90041FFF4FFEC000C2700FFFFD10000047E000000000000000000060103880242003100
    
    
    start   = datetime.utcnow() - timedelta(days=args.days);
    end     = datetime.utcnow()# - timedelta(days=120);
    
    sats = args.sats
    if args.verify==1:
      verify = True
    else:
      verify = False
    
    print("Verify satnogs get:", verify)
    #sats = Satellite.objects.filter(satnogs=True, active=True)
    #sats = Satellite.objects.filter(code="TITA")
    
    #dictionary with sended packets
    sentpackets = {}
    for s in sats:
        sentpackets[s] = MaxSizeList(30000)
        
    
    #user = User.objects.get(username="sa")   
    sendsession = requests.Session()
    #TODO replace with values from db.
    
    sendsession.auth = (args.user, args.password)
    sendsession.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json',})
    
    recsession = requests.session()

       
        
    for sat in sats:
                
      dtn = datetime.utcnow()
      
      #sat = Satellite.objects.get(code="LITUANICASAT2")
      #, 'vetted_status':"good"
      params = {'satellite__norad_cat_id':sat, 'start':start, 'end':end} 
      #Controlar rg.status_code rg.reason
      
      
      #url = "https://network.satnogs.org/api/data/?satellite__norad_cat_id=40014&start=2020-01-01+00%3A00"
      #url = "https://network.satnogs.org/api/data/"
      url = "https://network.satnogs.org/api/observations/"
      rg = recsession.get(url=url, params=params, verify=verify)#, 
      try:
        while rg!=None:
          datas = rg.json()
          print(len(datas))
          for data in datas:
            if len(data['demoddata'])>0:
              #Recorro las observaciones!
              for dd in data['demoddata']:
                dt=extractSatnogsURLDateTime(dd)
                if dt!=None:
                  #else de except
                  print("Se intentan cargar datos de ", dt, "satellite", sat)
                  if not (dt in sentpackets[sat]):
                      #El paquete no esta en memoria, esta ya en la bd?
                      if not rawInBd(sendsession, APIURL, sat, dt):
                        rgi = recsession.get(dd['payload_demod'], verify=verify)#, verify=False
                        dtn = datetime.utcnow()
                        try:
                          res = sendJsonDataPkt(APIURL,
                                                dtn , #captureddt
                                                dt, #packet
                                                sat, 
                                                rgi.content.hex(), 
                                                rgi.content.hex(), 
                                                False, 
                                                "SATNOGSWS",
                                                sendsession)
                          if res.status_code==status.HTTP_409_CONFLICT:
                              print("Duplicated", res)
                              sentpackets[sat].append(dt)
                          elif res.status_code==status.HTTP_201_CREATED:
                              print("Paquete ", dt, "cargado (NUEVO)")
                              sentpackets[sat].append(dt)
                          else:
                              print("Packet isn't accepted", res)
                        except Exception as e:
                          print("Exception sending data to rest service ", e);
                          #else:
                      else:
                        print("paquete",dt ,"previamente cargado...BD")
                        sentpackets[sat].append(dt) 
                  else:
                    print("paquete",dt ,"previamente cargado...en memoria")     
                else:
                  print("No se pudo obtener fecha")
          if (len(rg.links)==0) or (not('next' in rg.links)):
            rg=None
          else:          
            rg = recsession.get(rg.links['next']['url'], verify=verify)
        
      except Exception as ex:
        print(ex)
      
    
    print("Se cierran sesiones...")  
    sendsession.close()
    recsession.close()
    print("Sesiones cerradas")  


#Hacer de esto un script, por sus caracteristicas es complicado
#manejarlo como tarea dado que lanza un navegador.
class ISSTelemetryAdapter():
#class ISSTelemetryAdapter(app.Task):
    '''
    classdocs
    '''
    name = 'tasks.ISSTelemetryAdapter'

    def __init__(self):
        #driver ethos display 1
        loadDjangoApp()
        from Scripts.ISSDataDataCreation import create_iss_base_data
        create_iss_base_data()
        from selenium import webdriver
        self.dethosd1 = webdriver.Firefox()
        self.dethosd1.get("https://isslive.com/displays/ethosDisplay1.html")


    def run(self):
        
        
        lock_id = '{0}-lock-{1}'.format(self.name, "ISSTelemetryAdapter")
        #logger.debug('Importing feed: %s')
        print("ISSTelemetry starting...")
    
        #with memcache_lock(lock_id, self.app.oid) as acquired:
        #if acquired:
        from GroundSegment.models.Satellite import Satellite
        from Telemetry.models.TlmyVar import TlmyVar
        from Telemetry.models.TlmyVarType import CType
        
        iss = Satellite.objects.get(code="ISS")
        
        for tt in iss.tmlyVarType.all(): 
            #"//span[@field='NODE3000001']"
            search = "//span[@field='"+tt.tag.split('|')[0]+"']"
            value = self.dethosd1.find_element_by_xpath(search).text
            if value!="N/A" and value!=tt.tag.split('|')[0] and value!="":
                tvar = TlmyVar()
                tvar.code = tt.code
                tvar.tlmyVarType = tt
                if tt.ctype==CType.objects.get(code="float"):
                    #print("Valor a convertir:", value)
                    value = float(value)
                    
                tvar.setValue(value, datetime.now(utc))
                tvar.save()
                #print("Telemetria ", tvar.code, "valor", tvar.getValue())
                
        print("Telemetria ISS Procesada");        
    #else:
        #logger.debug('Feed %s is already being imported by another worker', feed_url)
    #    print("ISSTelemetry feed is already working...")
    
      
      
        
        


              
#app.tasks.register(ISSTelemetryAdapter())
#ISSTelemetryAdapter.delay()

