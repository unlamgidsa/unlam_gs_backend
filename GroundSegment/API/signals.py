from Telemetry.models.TlmyVar import TlmyVarManager, before_bulk_create
from Telemetry.models.TlmyVar import TlmyVar
from django.db.models.signals import post_save
from django.dispatch import receiver
#Django channels and websockets-----------------
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
#-----------------------------------------------

@receiver(before_bulk_create, sender=TlmyVarManager)
def TlmyVarHandler(sender, **kwargs):

    #TODO: ARTICULO EXTENSION => envio un 
    # group_send por cada variable, sobrecargo el redis
    # pero cada cliente no recibe una unica variable cada vez
    # sabra si tiene o no que informarla 

    tlmys           = kwargs["tlmys"]
    channel_layer   = get_channel_layer()
    
    #hasta aca solo llegan las que estan subscriptas a al menos 
    #un cliente, se hace un broadcasting general pero indivicualmente
    #cada variable

    #es importante ver que ya aqui ocurre una serializacion y posterior
    #desearlizacion, ver si es posible quitar la signal
    exTlmys = json.loads(tlmys)
    
    for tlmy in exTlmys:
        #Se envia al grupo cada telemetria individualmente
        async_to_sync(channel_layer.group_send)(
        "RTTelemetry", #esto seria el room.group_name 
        {
            "type": "aOnNewtlmy", #Function name!
            "tlmyVars": json.dumps(tlmy),               
            "tlmyVarsIds": tlmy["fullName"]
        }
    )

    
    





##Django channels, websockets
#@receiver(post_save, sender=TlmyVar)

# @receiver(before_bulk_create, sender=TlmyVarManager)
# def TlmyVarHandler(sender, instance, created, **kwargs):
#     if created:
#         #print("Cambio de telemetria detectado(Signal)")
#         channel_layer = get_channel_layer()
#         #Remplazar por el JSON correspondiente
#         data = instance.toJson()
#         instanceFullName = instance.getFullName()
        
#         #Aca se puede especificar a que grupo se manda en lugar de gossip?
        
#         async_to_sync(channel_layer.group_send)(
#             "RTTelemetry", #esto seria el room.group_name 
#             {
#                 "type": "onnewtlmy", #Function name!
#                 "tlmyVar": instanceFullName,
#                 #"room_id": room_id,
#                 #"username": self.scope["user"].username,
#                 "value": data
#             }
#         )
#         """
#         or async_to_sync(channel_layer.group_send)("chat", {"type": "chat.force_disconnect"})
#         channel_layer = get_channel_layer()
#             await channel_layer.send("channel_name", {
#                 "type": "chat.message",
#                 "text": "Hello there!",
#             })
#         """



# """
# #@receiver(post_save, sender=TlmyVar)
# def announce_new_tlmy(sender, instance, created, **kwargs):
#     if created:
#         print("Cambio de telemetria detectado")
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "gossip", 
#             {"type": "tlmyVarConsumer",
#             "event": "NewTlmyVar",
#             "tlmyVar":instance.code 
#             }

#         )
# """