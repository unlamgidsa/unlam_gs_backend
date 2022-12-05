'''
Created on 21 mar. 2022

@author: pabli
'''

import json
from channels.generic.websocket import WebsocketConsumer
import time
from datetime import datetime
from multiprocessing import Process, Lock
from django.utils import timezone
from asgiref.sync import async_to_sync


lock = Lock()

class TlmyConsumer(WebsocketConsumer):
  def connect(self):
    #print("Scope==>",self.scope)
    #client es ip y puerto, teoricamente identificaria univocamente un openmct
   
    clientid =  self.scope['client'][0]+"_"+str(self.scope['client'][1])
    print("Client id ip+port: ", clientid)
    #self.scope["headers"] <= informacion sobre la conexion
    #if self.scope["user"].is_anonymous:
    #        self.close()
    #else self.room_group_name = self.scope['url_route']['kwargs']['room_name']

  
    #self.group = "newTelemetry"
    self.room_name        ="RTTelemetry"
    self.room_group_name  = "RTTelemetry"
    self.tlmys = []  
    print("Se agrega el grupo RTTelemetry el canal", self.channel_name)
    #Primer parametro nombre del grupo, segundo el canal actual.
    #Verificar que informacion del cliente se tiene.

    #el grupo es mas grande, por cada grupo hay rooms
    async_to_sync(self.channel_layer.group_add)(
      "RTTelemetry",
      self.channel_name
    )
    
    self.accept()
    self.send(text_data= json.dumps({'type':'onconnect','message': 'connection accepted'}))

  def sendNews(self, obj, lock,tlmys, exTlmys):

      #
      try:
        if len(exTlmys)>0:
          dt = timezone.now()
          print("Las variables tardan esto en llegar aca, porque?===>>>>", (dt-datetime.fromisoformat(exTlmys[0]["created"])).total_seconds())

        
        pktlist = [] #list of dictionaries
        for tlm in tlmys:
          res = list(filter(lambda x:x["fullName"] == tlm, exTlmys))
          if(len(res)>0):
            pktlist.append(res[0])
        
        #print("La separacion de variables a informar se comio : {:.2f}".format(time.time()-arranque))  
              
        #Cual es la diferencia entre el tiempo que se marco como recibido y el momento donde se 
        #envian los paquetes?
        diffs = 0
        cont = 0
        dt = timezone.now()
        for p in pktlist:
          diffs += (dt-datetime.fromisoformat(p["created"])).total_seconds()
          cont=cont+1
        
        if cont!=0:
          med = diffs/cont
        else:
          med = 0
        print("Cada paquete tarde esto, se estan encolando?=>", med)  
        if obj!=None:
          #lock.acquire()
          try:
            obj.send(json.dumps(pktlist))
          finally:
            pass
            #lock.release()
        else:
          self.send(json.dumps(pktlist))
        print("El send fue ejecutado")
      except Exception as ex:
        print(ex)    
      #AsyncWebsocketConsumer se ejecutan realmente en paralelo
      #La realidad es que lo asincronico recien aparece recien aca, 
      #y no parece ser el problema de la degradacion del servicio.    
      
  
  
  def onNewtlmy(self, event):
    #print("####ON NEW TLMY###>>>>ROOM NAME: ", self.room_name)
    
    try:
      if not "tlmyVars" in event:
        print("Error, la signal viene con datos desconocidos")
      else:
        CON_PROCESO = True
        if CON_PROCESO:
          st = time.time()
          #result = Queue()
          p = Process(target=self.sendNews, args=(self, lock, self.tlmys, json.loads(event["tlmyVars"])))
          p.start()
          #p.join()
          print("respondido en paralelo...", (time.time()-st))
        else:
          self.sendNews(None, None, self.tlmys, json.loads(event["tlmyVars"]))  
    except Exception as ex:
      print(ex)
    
  def receive(self, text_data):
    # WebsocketConsumer.receive(self, text_data=text_data, bytes_data=bytes_data)
    # Aca subscribir variables
    #subscribe ${sat_name}.${tlmy_var}
    #TODO: Modificar por un json!
    response_text = "NO"
    
    cmd = text_data.split()[0]
    var = text_data.split()[1]

    #TODO: Controlar que sea comando valido y variable de telemetria real 
    if(cmd=="subscribe"):
      if not var in self.tlmys:
        print("Se subscribe var(sync)", var)
        self.tlmys.append(var) 
      else:
        print("Var ya existente", var)

      response_text = var
    elif (cmd=="unsubscribe"):
      print("Se desubscribe var")
      if var in self.tlmys:
        self.tlmys.remove(var)
      response_text = var
    else:
      print('Unknown command')
      response_text = 'Unknown command'
    
    self.send(json.dumps({"type":"response", "value":response_text}))
    
    #val = json.loads(text_data)["value"]

    #Proceso la funcion indicada en "type"
    #await self.channel_layer.group_send(
    #  self.group,
    #  {'type':'response', 'value':response_text}
    #)
    
  def response(self, event):
    valOther = event["value"]
    print("Recibido en Server KA==>>", valOther)
    text_data=json.dumps({"value":"keepAliveResponse"})
    self.send(text_data)
    print("<", text_data)

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(
      "RTTelemetry",
      self.channel_name
    )
    #await self.disconnect(close_code)