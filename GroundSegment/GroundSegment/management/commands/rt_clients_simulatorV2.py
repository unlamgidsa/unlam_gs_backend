from django.core.management.base import BaseCommand, CommandError
import threading
import time
import random
import json
from datetime import datetime
from django.utils import timezone
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar
import websocket
import time
import rel
import sys
import asyncio
#uvicorn asgi:application --port 8001 --host 0.0.0.0 --workers 4
class Command(BaseCommand):
    help = 'Start the RTClientsSimulator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_clients = 2
        self.last_pkt = timezone.now()

    def on_message(self, ws, message):
        
        #print("Recibido=>", message)
        #print("Recibido telemetria", message[0:10])
        
        rawmessage = message
        dt = timezone.now()
        message = json.loads(message)
        if ("message" in message) and (message["message"]=="connection accepted") :
            print(rawmessage)
            print("Conexion aceptada, subscribo hasta 30 variables")
            #subscribir todo
            max = len(self.tlmyList)
            if max>self.totalVars: #tipicamente 30
                max = self.totalVars
            
            for i in range(max):
                tlmSub = self.sat_code+"."+self.tlmyList[random.randrange(0, len(self.tlmyList))]
                #print("intento subscribir ", tlmSub)
                ws.send("subscribe" +" "+tlmSub)


        else:
            #calcular la media de diferencia
            
            #En realidad se debe tomar solo el primer mensaje,
            #el resto se encolan pero ese es problema del cliente, no del servidor
            if(message!=""):
                
                #print("Recibiendo algo concreto", datetime.now(), "tamanio", len(message))
                if ws.selected:
                    totalseconds = 0
                    for r in message:
                        totalseconds += (dt-datetime.fromisoformat(r["created"])).total_seconds()
                    
                    print("diffs=>", totalseconds/len(message))
            else:
                print("Empty message")    
            
                

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")
        
    def add_arguments(self, parser):
        pass
        #harcode por ahora el nombre del satelite
        #parser.add_argument('sat_code', nargs='+', type=int)

    def handle(self, *args, **options):
        #Que sea parametro
        url = "ws://127.0.0.1:8001/ws/RTTelemetry/"
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        
        total_clients           = 600
        simulation_seconds      = 500
        sleep                   = 20
        TOTALVARS               = 30    
        sat_code                = "RTEmuSat"
        self.total_clients      = total_clients-1
        
        self.totalVars          =  TOTALVARS
        self.sat_code           = "RTEmuSat" 
        self.tlmyList         = Satellite.objects.get(code=sat_code).tmlyVarType.all().values_list('code', flat=True)

        for i in range(total_clients):
            ws = websocket.WebSocketApp(url, on_message=self.on_message)
            ws.selected = False
            #Tomo uno random, el de la mitad para medir demoras
            if i==(total_clients//2):
                ws.selected = True
 
            ws.run_forever(dispatcher=rel)  
        rel.signal(2, rel.abort)  # Keyboard Interrupt  
        rel.dispatch()  
        
        