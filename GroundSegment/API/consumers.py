'''
Created on 21 mar. 2022

@author: pabli

VER: https://jaydenwindle.com/writing/django-websockets-zero-dependencies/
'''

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time
from datetime import datetime
from multiprocessing import Process
from django.utils import timezone
from asgiref.sync import async_to_sync
import asyncio

#Usar para sincronizar llamadas a las base de datos
#justificar porque esto se comparte via DB en lugar
#de via REDIS 
from channels.db import database_sync_to_async
from API.models import SubscribedTlmyVar, WSClient

WSClient.objects.all().delete()

class AsyncTlmyConsumer(AsyncWebsocketConsumer):
  @database_sync_to_async
  def addClient(self):
    ip = self.scope['client'][0]
    port = self.scope['client'][1]
    #TODO Ver que informacion util se puede persistir
    #self.scope["headers"] <= informacion sobre la conexion
    #if self.scope["user"].is_anonymous:
    #        self.close()
    #else self.room_group_name = self.scope['url_route']['kwargs']['room_name']
    self.ws = WSClient(ipv4=ip, port=port)
    self.ws.save()

  
  @database_sync_to_async
  def deleteClient(self):
    self.ws.delete()

  @database_sync_to_async
  def addSubscrivedTlmyVar(self, fullname):
    subscribedTlmyVar, created = SubscribedTlmyVar.objects.get_or_create(fullname=fullname, wsClient=self.ws)
    if not created:
      print("No creada, esta duplicada")
    subscribedTlmyVar.save() 
    return None

  @database_sync_to_async
  def deleteSubscrivedTlmyVar(self, fullname):
    try:
      self.ws.subscribedTlmyVar.get(fullname=fullname).delete()
    except SubscribedTlmyVar.DoesNotExists:
      print("Se intenta desuscribir var no subscripta previamente")
    return None

  
  async def connect(self):
    #print("Scope==>",self.scope)
    #client es ip y puerto, teoricamente identificaria univocamente un openmct
    self.ws = None
    self.clientid =  self.scope['client'][0]+"_"+str(self.scope['client'][1])
    print("Client id ip+port: ", self.clientid)
    await self.addClient()
    #self.group = "newTelemetry"
    self.room_name        ="RTTelemetry"
    self.room_group_name  = "RTTelemetry"
    self.tlmys = set()
    print("Se agrega el grupo RTTelemetry el canal", self.channel_name)
    #Primer parametro nombre del grupo, segundo el canal actual.
    #Verificar que informacion del cliente se tiene.

    #el grupo es mas grande, por cada grupo hay rooms
    await self.channel_layer.group_add(
      "RTTelemetry",
      self.channel_name
    )
    
    await self.accept()
    await self.send(text_data= json.dumps({'type':'onconnect','message': 'connection accepted'}))

  async def sendNews(self, tlmys, event):
      tlmyVarsIds = json.loads(event["tlmyVarsIds"])
      try:
        if len(tlmyVarsIds)>0:
          dt = timezone.now()
          #print("Las variables tardan esto en llegar aca, porque?===>>>>", (dt-datetime.fromisoformat(exTlmys[0]["created"])).total_seconds())
          exTlmys = json.loads(event["tlmyVars"])
      
          #Extraigo ids
          exTlmysSet = set(tlmyVarsIds)
          intersection_ids = tlmys & exTlmysSet
          #Todo muy lindo pero ahora hay que juntar las variables por clave
          pktlist = [x for x in exTlmys if x["fullName"] in intersection_ids]
        
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
        #print("Cada paquete tarde esto, se estan encolando?=>", med)  
        await self.send(json.dumps(pktlist))
        #print("Paquete enviado")
      except Exception as ex:
        print(ex)    
      
  
  
  async def aOnNewtlmy(self, event):
    #print("####ON NEW TLMY###>>>>ROOM NAME: ", self.room_name)
    try:
      if not "tlmyVars" in event:
        print("Error, la signal viene con datos desconocidos")
      else:
        await self.sendNews(self.tlmys, event)
        
    except Exception as ex:
      print(ex)
    
  async def receive(self, text_data):
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
        print("Se subscribe var", var)
        self.tlmys.add(var) 
        #TODO: Revisar si conviene doble implementacion, tener en memoria y 
        #en base a donde esta subscripto
        await self.addSubscrivedTlmyVar(var)
        #¿Avisar al grupo de que hay nuevas telemetrias o es muy complejo?
      else:
        print("Var ya existente", var)

      response_text = var
    elif (cmd=="unsubscribe"):
      print("Se desubscribe var")
      if var in self.tlmys:
        self.tlmys.remove(var)
        await self.deleteSubscrivedTlmyVar(var)
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
    
  async def response(self, event):
    valOther = event["value"]
    print("Recibido en Server KA==>>", valOther)
    text_data=json.dumps({"value":"keepAliveResponse"})
    await self.send(text_data)
    print("<", text_data)

  async def disconnect(self, close_code):
    #por CASCADE deberia desubscribir todo
    await self.deleteClient()
    #for var in self.tlmys:
    #  await self.deleteSubscrivedTlmyVar(var, self.clientid)
    
    await self.channel_layer.group_discard(
      "RTTelemetry",
      self.channel_name
    )
    #await self.disconnect(close_code)