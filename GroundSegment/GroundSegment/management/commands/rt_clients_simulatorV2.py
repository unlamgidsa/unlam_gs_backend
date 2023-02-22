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
import _thread
import time
import rel



class Command(BaseCommand):
    help = 'Start the RTClientsSimulator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._i = 1    
        self._lastdiff = 0
        self.total_clients = 2

    def on_message(self, ws, message):
        
        #print("Recibido=>", message)
        #print("Recibido telemetria", message[0:10])
        
        rawmessage = message
        message = json.loads(message)
        if ("message" in message) and (message["message"]=="connection accepted") :
            print(rawmessage)
            print("Conexion aceptada, subscribo hasta 30 variables")
            #subscribir todo
            max = len(self.tlmyList)
            if max>self.totalVars:
                max = self.totalVars
            for i in range(max):
                tlmSub = self.sat_code+"."+self.tlmyList[random.randrange(0, len(self.tlmyList))]
                #print("intento subscribir ", tlmSub)
                ws.send("subscribe" +" "+tlmSub)
        else:
            #calcular la media de diferencia
            #print("Recibiendo algo", datetime.now())
            seconds = 0
            self._i += 1
            dt = timezone.now()
            for r in message:
                seconds += (dt-datetime.fromisoformat(r["created"])).total_seconds()
            #print("=>", len(rawmessage), "diffs:", seconds/len(message) )
            self._lastdiff = seconds/len(message)
            if (self._i % self.total_clients) == 0:
                print("diffs=>", self._lastdiff)

            
        
            
                


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
        url = "ws://127.0.0.1:8000/ws/RTTelemetry/"
        

        total_clients           = 1
        simulation_seconds      = 500
        sleep                   = 20
        TOTALVARS               = 30    
        sat_code                = "RTEmuSat"
        self.total_clients      = total_clients-1
        
        self.totalVars          =        TOTALVARS
        self.sat_code           = "RTEmuSat" 
        self.tlmyList         = Satellite.objects.get(code=sat_code).tmlyVarType.all().values_list('code', flat=True)

        
        for i in range(total_clients):
            ws = websocket.WebSocketApp(url, on_message=self.on_message)
            ws.run_forever(dispatcher=rel)  
        rel.signal(2, rel.abort)  # Keyboard Interrupt  
        rel.dispatch()  
        
        