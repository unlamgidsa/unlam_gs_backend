"""
Created on 17 mar. 2022

@author: Pablo Ferreira. Pablo Soligo
"""

#Se muda a commands siguiendo este tutorial:
#https://docs.djangoproject.com/en/1.10/howto/custom-management-commands/

from django.core.management.base import BaseCommand, CommandError
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.FrameType import FrameType
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SubSystem import SubSystem

from Utils.PktsHelpers import sendJsonDataPkt
from GroundSegment.settings import APIURL
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from struct import pack, calcsize
from math import sin
from time import sleep, mktime, time
from random import random
from binascii import unhexlify, hexlify
import requests
from rest_framework import status
from GroundSegment import config




#python manage.py rt_sat_simulator
#Comenzamos a emprolijar los comandos, ahora deberian estar todos
#en commands
def getUTCTimeStamp(kwargs):
    return int(time())


def getSenoidalValue(kwargs):
    # Time modificado para que la funcion se vea continua a pesar de un SLEEP_TIME grande
    return sin(kwargs["unixTimeStamp"] / 10 * (1 / kwargs["SLEEP_TIME"]))

#frame publico
def getRandom(kwargs):
    return random()

# Se crea una trama de telemetria a partir de una lista de diccionarios python
        # Cada elemento de la lista es un campo y los diccionarios internos determinan
        # como se construye el campo Valor, Tipo y encoding. (El nombre es descriptivo)
frm1Dic = [ {"name": "SinValue1", "Value": getSenoidalValue, "Ctype": "f", "encoding": "<"},
            {"name": "SinValue2", "Value": getSenoidalValue, "Ctype": "f", "encoding": "<"},]
    
#frm1Dic = [
#    # El unix timestamp lo determina una funcion, es dinámico
#    {"name": "UnixTimeStamp", "Value": getUTCTimeStamp, "Ctype": "I", "encoding": "<"},
#    # El frametype es hardcode = 1, cuando desarrollemos otros frames le ponemos 2,3,4 etc
#    {"name": "FrameType", "Value": 1, "Ctype": "H", "encoding": "<"},
#    {"name": "Var1", "Value": getRandom, "Ctype": "f", "encoding": "<"},
#    {"name": "Var2", "Value": 0, "Ctype": "i", "encoding": "<"},
#    {"name": "Var3", "Value": 0, "Ctype": "i", "encoding": "<"},
#    {"name": "SinValue", "Value": getSenoidalValue, "Ctype": "f", "encoding": "<"},
#]


class Command(BaseCommand):
    help = 'Start the RTSatSimulator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_arguments(self, parser):
        pass
        #harcode por ahora el nombre del satelite
        #parser.add_argument('sat_code', nargs='+', type=int)

    def utf8len(self, s):
        return len(s.encode('utf-8'))


    def handle(self, *args, **options):
         # Default parameters for fast test without command line arguments
        frm1Dic = []
        #Remplazar hardcode por parametro
        SLEEP_TIME      = 20
        NB_ITERATIONS   = 100
        TOTAL_VARS      = 10
        
        for i in range(TOTAL_VARS):
            if(i%2==0):
                frm1Dic.append({"name":  "SinValue"+str(i), "Value": getSenoidalValue, "Ctype": "f", "encoding": "<"})
            else:
                frm1Dic.append({"name":  "SinValue"+str(i), "Value": 1.5, "Ctype": "f", "encoding": "<"})



        createNewTypes=True
        
        if(createNewTypes):
            sat = self._init_database_(frm1Dic)
        else:
            sat_code = "RTEmuSat"
            sat = Satellite.objects.get(code=sat_code)
        
        
        t1 = time()
        t2 = time()
        
        #TODO Remplazar el falso por parametros
        if(False):
            SLEEP_TIME = int(sys.argv[1])
            NB_ITERATIONS = int(sys.argv[2])

        # Se crea una sesion (tambien pasar por argumentos)
        USER        = config.GS_API_USER
        PASSWORD    = config.GS_API_PASSWORD
        sendsession = requests.Session()
        # TODO replace with values from db.
        sendsession.auth = (USER, PASSWORD)
        sendsession.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
         #TODO: Remplazar para que no sea hardcode
        sleepDif    = 0
        INTEGER     = 0
        FLOAT       = 1   
        i = 0
        # Solo para plotear y ver resultado, esto desaparece en version final!
        pltValues = []
        context = {}  # Conjunto de parametros para la funcion senoidal

        for i in range(NB_ITERATIONS):
            # Contexto como parametro de funciones, por ahora solo un valor, la fecha
            # agregar lo necesario para que la funcion opere de manera
            # correcta con frecuencias distintas

            buffer = bytes()  # buffer donde concatenar las binarizaciones de cada dato

            for fieldsDic in frm1Dic:
                format = ""

                # Note que cada campo es un diccionario con toda la informacion para binarizar.
                # Python pack parece no aceptar binarizacion con distintos enconding, por tanto se
                # tiene que hacer campo a campo y concatenar en la trama final

                # Campos opcionales
                if "len" in fieldsDic:
                    format += fieldsDic["len"]
                if "encoding" in fieldsDic:
                    format += fieldsDic["encoding"]

                # Agrego a formato el Ctype (tiene que estar)
                format += fieldsDic["Ctype"]

                if callable(fieldsDic["Value"]):
                    # Mejor no modificar acá el time si lo vamos a meter en "unixTimeStamp", nombre que suena al time sin modificar
                    context["unixTimeStamp"] = int(time())
                    context["SLEEP_TIME"] = SLEEP_TIME
                    value = fieldsDic["Value"](context)
                else:
                    value = fieldsDic["Value"]

               

                # Concateno bytes
                buffer += pack(format, value)

            self.stdout.write("Iteracion: "+str(i))
            # Muestro el binario final
            #self.stdout.write("Trama binaria:"+str(buffer))
            # Transformo el binario en hexadecimal texto para posteriormente llamar al webservice
            # Ademas sirve para control
           
            hexstr = hexlify(buffer)
            #self.stdout.write("Trama hexadecimal (Para webservice): "+str(hexstr))
            # # rebinarizo para control binascii.unhexlify(validated_data['strdata'])
            # print("Trama rebinarizada: ", unhexlify(hexstr))

            # Se crea e intenta enviar un json-data-packet con el contenido del buffer
            
            try:
                
                res = sendJsonDataPkt(
                    APIURL,
                    datetime.utcnow(),
                    datetime.utcnow(),
                    str(sat.noradId),
                    buffer.hex(),
                    buffer.hex(),
                    True,
                    "TEST",
                    sendsession,
                )
                
                self.stdout.write("Tamaño del paquete:" + str(self.utf8len(buffer.hex())))
                if res.status_code == status.HTTP_409_CONFLICT:
                    self.stdout.write("Duplicated "+ str(res))
                elif res.status_code == status.HTTP_201_CREATED:
                    t2 = time()
                    self.stdout.write("Created "+str(res)+" time b/pack: "+ "{:.2f}".format(t2-t1)+", time dif: "+str(SLEEP_TIME-(t2-t1)))
                else:
                    self.stdout.write("Packet isn't accepted "+str(res))
            except Exception as e:
                self.stdout.write("Exception sending data to rest service: "+str(e))

            sleepDif = SLEEP_TIME-(t2-t1)
            t1 = t2
            self.stdout.write("SleepDif: {:.2f}".format(sleepDif))
            if(sleepDif<0):
                sleepDif=0
            sleep(sleepDif)
        
        print("Fin")
    

    def _init_database_(self, frm1Dic):
        i = 0
        CType.createBasics()
        sat_code = "RTEmuSat"
        try:
            sat = Satellite.objects.get(code=sat_code)
        except Satellite.DoesNotExist as ex:
            sat = Satellite()
            sat.code        = sat_code
            sat.description = sat_code
            sat.noradId     = 0
            sat.state          = SatelliteState.objects.first()
            sat.inContact      = False
            sat.save()
    
                    
        
        self.stdout.write(sat.code)
        tvts = sat.tmlyVarType.all()
        for tvt in tvts:
            #Si existe el tipo le borro todas las tlmyVars y luego borro el tipo
            try:
                #tt = sat.tmlyVarType.get(code=frmTvt["name"])
                #Elimino las variables
                tvt.tlmyVars.all().delete()
                #Elimino el tipo
                tvt.delete()
            except TlmyVarType.DoesNotExist:
                self.stdout.write("Telemetria no existente")

        #Elimino los raw del satelite
        sat.rawdatas.all().delete()    

        #Ahora vuelvo a crear
        current_position = 0
        for frmTvt in frm1Dic:
            subsystem, created      = SubSystem.objects.get_or_create(code="ALL", description="ALL")
            if(created):
                subsystem.save()
            #Tienen que existir, dar de alta por script que peine toda las posibilidades
            frameType, created      = FrameType.objects.get_or_create(aid=-1, description="NoFrame", satellite=sat)
            if(created):
                frameType.save()

            ctype                   = CType.objects.get(format=frmTvt["encoding"]+frmTvt["Ctype"])
            um, created             = UnitOfMeasurement.objects.get_or_create(code="N/A", description="N/A")
            if(created):
                um.save()
            
            #Siempre va a crear si se ejecuto el codigo anterior
            tlv, created = TlmyVarType.objects.get_or_create(code=frmTvt["name"],
                                                description=frmTvt["name"],
                                                satellite=sat,
                                                position=current_position,
                                                subPosition=0,
                                                bitsLen=ctype.length*8,
                                                subsystem=subsystem,
                                                unitOfMeasurement=um,
                                                ctype=ctype,
                                                frameType=frameType)
            current_position += ctype.length
            tlv.save()
            if (i%100) == 0:
                self.stdout.write("tipo de telemetria "+tlv.code+" creado")
        return sat


