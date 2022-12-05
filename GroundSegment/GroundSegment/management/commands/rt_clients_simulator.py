
from functools import reduce
from platform import release
from django.core.management.base import BaseCommand, CommandError
import websocket
import threading
import time
import random
import json
from datetime import datetime
from django.utils import timezone
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar

#websocket.enableTrace(True)


glock = threading.Lock()


class WsClient(object):
    def __init__(self, url, sat_code, tlmyList, totalVars):
        self.url = url
        self.stopped = False
        self.ws = websocket.WebSocket(enable_multithread=True) 
        
        self.tlmyList  = tlmyList
        self.current_tlmy_list = []
        self.sat_code  = sat_code
        self.difs = []
        self.totalVars = totalVars
        self.__used = False

    def getVars(self):
        return len(self.current_tlmy_list)

    def __add(self, x, y):
        return x+y

    def getDifs(self):
        val = 0
        ld = len(self.difs)
        if(ld>0):
            val = reduce(self.__add, self.difs)/ld
            self.__used = True
            
        
        return val

    def setStopped(self, value):
        
        try:
            self.stopped = value
        finally:
            pass

    def _getStopped(self):
        lstopped = True
        
        try:
            lstopped = self.stopped
        finally:
            pass
        return lstopped


    def start(self):
        

        self.ws.connect(self.url)
        self.ws.settimeout(20)
        random.seed(1)
        subscribe   = "subscribe"
        unsubscribe = "unsubscribe"
        while(self.ws.connected and not self._getStopped()):
            try:
                recv = self.ws.recv()
                #print("Recibido=>", recv)
                recv = json.loads(recv)
                if ("message" in recv) and ((recv["message"]=="connection accepted")or((recv["message"]=="connection accepted sync"))) :
                    #print("Conexion aceptada, subscribo hasta 30 variables")
                    #subscribir todo
                    max = len(self.tlmyList)
                    if max>self.totalVars:
                        max = self.totalVars
                    for i in range(max):
                        tlmSub = self.sat_code+"."+self.tlmyList[random.randrange(0, len(self.tlmyList))]
                        #print("intento subscribir ", tlmSub)
                        self.ws.send(subscribe +" "+tlmSub)
                        self.current_tlmy_list.append(tlmSub)

                else:
                    #print("Se reciben novedades, tam del paquetes ", len(recv))
                    try:
                        dt = timezone.now()
                        if self.__used:
                            self.difs = []
                            self.__used = False
                        totaldiff = 0.0
                        for r in recv:
                            seconds = (dt-datetime.fromisoformat(r["created"])).total_seconds()
                            totaldiff+= seconds
                            #print("diffs=>", seconds)
                        #diff = row[0]-datetime.fromisoformat(recv["created"])
                        diff = totaldiff/len(recv)
                        #print("Diff=>", diff)
                        #print("Novedad, DIFF:", ts-tag)
                        glock.acquire()
                        try:
                            self.difs.append(diff)
                        finally:
                            glock.release()
                    except Exception as ex:
                        print(str(ex))
                  #Si se recibe ok de subscription agrego a lista
            except Exception as ex:
                pass
                #print(str(ex)), connection timeout es normal
                #No subscribo ni desubscribo nada para no complicar.
                """
                if random.randrange(0, 10)==5:
                    tlmSub = self.sat_code+"."+self.tlmyList[random.randrange(0, len(self.tlmyList))]
                    #print("intento subscribir ", tlmSub)
                    self.ws.send(subscribe +" "+tlmSub)
                elif random.randrange(0, 10)==5:
                    if(len(self.current_tlmy_list)>0):
                        elim=self.current_tlmy_list[random.randrange(0, len(self.current_tlmy_list))]
                        self.ws.send(unsubscribe+" "+self.sat_code+"."+self.tlmyList[random.randrange(0, len(self.tlmyList))])
                """
        if self.ws.connected:
            self.ws.close()



class Command(BaseCommand):
    help = 'Start the RTClientsSimulator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_arguments(self, parser):
        pass
        #harcode por ahora el nombre del satelite
        #parser.add_argument('sat_code', nargs='+', type=int)

    def handle(self, *args, **options):
        #Que sea parametro
        total_clients           = 1
        simulation_seconds      = 500
        sleep                   = 20
        TOTALVARS               = 30     
        sat_code                = "RTEmuSat"

        
        clients = []
        #url = "ws://127.0.0.1:8052/ws/RTTelemetry/"
        #url = "ws://127.0.0.1:8000/ws/RTTelemetry/"
        url = "ws://127.0.0.1:8000/ws/SyncRTTelemetry/"
        tlmyList         = Satellite.objects.get(code=sat_code).tmlyVarType.all().values_list('code', flat=True)
        totalVars = 0
        totalDifs = 0
        print("Cantidad de conexiones, cantidad de variables subscriptas, diferencia de tiempo")
        for i in range(total_clients):
            wsc = WsClient(url, sat_code, tlmyList, TOTALVARS)
            threading.Thread(target=wsc.start).start()
            clients.append(wsc)
            #print("Total clientes: ", len(clients))
            
            time.sleep(sleep)
            
            totalDifs = 0
            for c in clients:
                glock.acquire()
                try:
                    totalDifs += c.getDifs()
                finally:
                    glock.release()

            logcad = str(len(clients))+";"+str(len(clients)*TOTALVARS)+ ";"+"{:.2f}".format(totalDifs)
            print(logcad)
        #Log.create("CLIENT_SIM", logcad, module, Log.INFORMATION).save()
        for i in range(simulation_seconds):
            totalDifs = 0
            for c in clients:
                totalDifs += c.getDifs()
                    

            logcad = str(len(clients))+";"+str(len(clients)*TOTALVARS)+ ";"+"{:.2f}".format(totalDifs)
            print(logcad)
            time.sleep(1)

        while(len(clients)>0):
            wsc = clients.pop()
            wsc.setStopped(True)
            time.sleep(sleep)