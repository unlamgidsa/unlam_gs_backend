"""
@package docstring
Created on 15 de nov. de 2016
@author: Pablo Soligo

Interface con UHF y futuro procesador de telemetria. Conecta con un servidor TCP/IP provisto por el fabricante de la 
antena. El servidor envia paquetes tcp/ip tan pronto como los tiene disponible. La comunicacion es bidireccional y acepta 
telecomandos, eso aun no esta implementado.

TESTING: Puede ser testeado perfectamente usando un servidor TCP/IP de test del tipo packetsender 
    ->https://packetsender.com/
"""
import socket
from struct import unpack, pack
#import crcmod
import time
import datetime

from django.conf import settings
import os
import sys

from django.utils import timezone

from array import array
import binascii

from binascii import hexlify, unhexlify

from django.core.exceptions import ObjectDoesNotExist






#ubuntumate@VBUbuntumate:~/Downloads/CheckoutBox/Software$ java -jar start.jar
#C:\Users\pabli\Documents\Programas\CheckoutBox\Software java -jar start.jar
#python Main.py CUBESAT o SIMULATION

"""

cd /home/ubuntumate/git/GroundSegment/GroundSegment/TlmyCmdProcessor/
Ejemplo de ejecucion 
>python TlmyCmdProcessor.py "SIMULATION" "FS2017" 

Deprecated: Ya no es necesario indicar el path, lo toma del directorio de ejecucion del fuente 
"C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
>python3.4 TlmyCmdProcessor.py "SIMULATION" "FS2017" 

Deprecated: Ya no es necesario indicar el path, lo toma del directorio de ejecucion del fuente "/home/ubuntumate/git/GroundSegment/GroundSegment/TlmyCmdProcessor" 
"""



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def is_set(x, n):
    return x & 2**n != 0 




"""Servicio, aplicacion encargada de decodificar, trasnformar y persistir la telemetria del satelite y de codificar y transmitir los 
telecomandos.
@param source Indica si la ejecucion es para servir a una simulacion o datos reales. Los paquetes persistidos quedan con esta cadena como marca
para uso futuro y especialmente para poder distinguir datos simulados de datos reales.
@param satellite Codigo de satelite con el que se esta comunicando. El satelite tiene que estar dado de alta en el catalogo. La trama de telemetria sera
decodificada en funcion de la configuracion de variables de telemetria del satelite indicado como parametro
"""



if __name__ == '__main__':
    
    PosFrameCommand         = 0
    LenFrameCommand         = 1
    
    PosFrameLen             = PosFrameCommand+LenFrameCommand
    LenFrameLen             = 4
    
    PosDataRate             = PosFrameLen+LenFrameLen
    LenDataRate             = 4
    
    PosModuluationNameLen   = PosDataRate+LenDataRate 
    LenModuluationNameLen   = 1
    
    PosModulationName       = PosModuluationNameLen+LenModuluationNameLen
    LenModulationName       = 0
    
    PosRSSI                 = PosModulationName+LenModulationName 
    LenRSSI                 = 8
    
    PosFrequency            = PosRSSI+LenRSSI
    LenFrequency            = 8
    
    PosPktLen               = PosFrequency+LenFrequency
    LenPktLen               = 2


    
    """Funcion principal del servicio, aplicacion encargada de decodificar, transformar y persistir la telemetria del satelite y de codificar y transmitir los 
    telecomandos.
    @param source Indica si la ejecucion es para servir a una simulacion o datos reales. Los paquetes persistidos quedan con esta cadena como marca
    para uso futuro y especialmente para poder distinguir datos simulados de datos reales.
    @param satellite Codigo de satelite con el que se esta comunicando. El satelite tiene que estar dado de alta en el catalogo. La trama de telemetria sera
    decodificada en funcion de la configuracion de variables de telemetria del satelite indicado como parametro
    """
    
    
    
    """
    Valores por default para guardado 
    de telemetria cruda (Marcar si el origen de la telemetria es simulado o real)
    """
    
    """Obtiene el path del proyecto segun carpeta de ejecucion"""
    proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = "SIMULATION"
    satellite = "FS2017"
    module = "TlmyCmdProcessor"
    

        
    
    if len(sys.argv)>1:
        source      = sys.argv[1]
        satellite   = sys.argv[2] 
    
    #https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
    
    
    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
    sys.path.append(proj_path)
    os.chdir(proj_path)
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from GroundSegment.Utils.Console import Console, NORMAL, WARNING, ERROR
    
   
    
    try:
        #Si me desconecto intento nuevamente conectarme despues de un sleep
        #y asi in eternum....
        
        Console.log("Reading configuration..")
        
        
        from GroundSegment.models.Satellite import Satellite
        from GroundSegment.models.TlmyRawData import TlmyRawData
        from GroundSegment.models.Parameter import Parameter
        from GroundSegment.models.TlmyVarType import TlmyVarType
        from GroundSegment.models.Log import Log
        from GroundSegment.models.Watchdog import Watchdog
        from GroundSegment.Utils.Utils import *
        from GroundSegment.models.DownlinkFrame import DownlinkFrame 
        from GroundSegment.Managers.CommandManager import CommandManager
        from GroundSegment.Utils.BColor import bcolors
        from GroundSegment.models.FrameType import FrameType
        from GroundSegment.models.TlmyVar import TlmyVar
        """
        Si el watchdog no fue creado aun en ejecuciones anteriores lo creo ahora
        """
        
        wd, created = Watchdog.objects.get_or_create(
                                        code='TlmyCmdProcessor',
                                        description='Watchdog del procesador de telemetria y telecomandos',
                                        module="TlmyCmdProcessor",
                                        tolerance=10,
                                    )   
        
        
        
       
        """
        Log guardar en el registro de log los sucesos que se consideren relevante para futura autoria o debug
        """
        Log.create("TlmyCmdProcessor started", "The uhf interface module was started", module, Log.INFORMATION).save()

        sat     = Satellite.objects.get(code=satellite)
        cmdmgr  = CommandManager(sat)
        
        """
        Bucle infinito, el software debe funcionar 7x24, si el software de la antena no estuviera 
        funcionando simplemente se duerme un tiempo parametrizable y vuelve a intentar la conexion
        hasta que este disponible. Dado que no es posible instalarlo como servicio, el watchdog se 
        realizar manualmente.
        """
        
        
            
        while True:
            """
            Limite de conexiones fallidas antes de recargar configuracion...
            
            """
            """
            Cargo todos los parametros de configuracion del sistema
            """
            
            """Deprecated, ahora el ip/puerto del cortex o equipo UHF es atributo del satelite"""
            uhfServerIp             = loadOrCreateParam("UHF_SERVER_IP", "GroundStation", "127.0.0.1", "IP del servidor TCP de la antena UHF")
            uhfServerPort           = loadOrCreateParam("UHF_SERVER_PORT", "GroundStation", "3210", "Puerto del servidor TCP de la antena UHF")    
            
            
            BUFFER_SIZE             = loadOrCreateParam("UHF_BUFFER_SIZE", "GroundStation", "1024", "Tamanio del buffer del cliente TCP")
            DISCONNECTION_SLEEP     = loadOrCreateParam("UHF_DISCONNECTION_SLEEP", "GroundStation", "10", "Tiempo en que se duerme la aplicacion ante una desconexion a la espera de volver a intentar")
            cls()
            Console.log("Done..trying to connect ip "+uhfServerIp+" ,port "+uhfServerPort)
            
            unconnectionLimit       = 0
            i = 0
            while unconnectionLimit<10:
                cls()
                Console.log("Create o recreate socket...", str(datetime.datetime.utcnow()))
                
                """
                Creo el socket -Cliente- que se conectara al software de la antena
                """            
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    """
                    Precargo todas los tipos variables de telemetria del satelite enviado argumento, lo hago 
                    aqui para hacerlo solo una vez, para mejorar el software se deberia pensar en una recarga cada intervalo
                    de tiempo determinado por si cambian la configuracion tomar los cambios
                    """
                    
                    #Log.create("LoadTlmy", "Load telemetry var types, count: "+str(len(telvars)), module, Log.INFORMATION).save()
    
                    
                    
                    """
                    Intento conectarme segun ip y puerto configurado, si la configuracion 
                    estuviera mal o no estuviera el servidor levantado el componente
                    de socket informa mediante exception, la misma es trapeada para volver
                    a intentar ciclicamente (Informe de error mediante)
                    """
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
                                Buena o mala la telemetria fue recibida, reseteo el watchdog
                                """
                                wd.reset()
                                
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
                                    #Console.log("--------------------Data Received-------------------")
                                    
                                    
                                    #print("\nData Received("+str(timezone.datetime.utcnow() )+"), Tamano: ", , "\nData->", chunk)
                                    
                                    data = TlmyRawData()
                                    data.source = source
                                    data.data = chunk
                                    data.processed = False
                                    data.save()
                                    
                                    startproctime = timezone.now()
                                    
                                    framecommand        = unpack("<B",chunk[PosFrameCommand:PosFrameCommand+LenFrameCommand])[0] 
                                    frameLength         = unpack("<I",chunk[PosFrameLen:PosFrameLen+LenFrameLen])
                                    datarate            = unpack("<I",chunk[PosDataRate:PosDataRate+LenDataRate])
                                    modulationnamelen   = (unpack("<B",chunk[PosModuluationNameLen:PosModuluationNameLen+LenModuluationNameLen]))[0]
                                    modulationname      = chunk[PosModulationName:PosModulationName+modulationnamelen] 
                                    PosRSSI             = PosModulationName+modulationnamelen 
                                    rssi                = unpack("<d", chunk[PosRSSI:PosRSSI+LenRSSI])
                                    PosFrequency        = PosRSSI+LenRSSI
                                    freq                = unpack("<d", chunk[PosFrequency:PosFrequency+LenFrequency])
                                    PosPktLen           = PosFrequency+LenFrequency
                                    pktLen              = unpack("<H",  chunk[PosPktLen:PosPktLen+LenPktLen])
                                    PosUtcTime          = PosPktLen+pktLen[0]
                                    LenUtcTime          = 4
                                    
                                    PosPayload = PosPktLen+int(LenPktLen)
                                    ax25 = chunk[PosPayload:PosPayload+pktLen[0]]
                                    
                                    
                                    destination  = ax25[0:7]
                                    asource      = ax25[7:7+7]
                                    control      = ax25[7+7:7+7+1]
                                    protocol     = ax25[7+7+1:7+7+1+1]
                                    
                                    #A8 A4 B0 AA AC 40 60 40 40 40 40 40 40 E1 03 F0 02 03 83 A5
                                         
                                    vardataoffset = 7+7+1+1 #16
                                    payload = ax25[ vardataoffset: ]
                                    
                                    pn = unpack("<H",  payload[1:3])
                                    
                                    
                                    frameTypeId = payload[0]
                                    
                                    #print(framecommand, ", ", frameLength, ", ", datarate, ", ", modulationname, "rssi", rssi, "Freq ", freq, "PktLen", pktLen)
                                    
                                    dl = DownlinkFrame()
                                    
                                    dl.frameCommand     = framecommand
                                    dl.frameLength      = frameLength[0]
                                    dl.dataRate         = datarate[0]
                                    dl.modulationName   = str(modulationname)
                                    dl.rssi             = rssi[0]
                                    dl.frequency        = freq[0]
                                    dl.packetLength     = pktLen[0]
                                    dl.satellite        = sat
                                    dl.ax25Destination  = "Pending"#destination.decode("utf-8") 
                                    dl.ax25Source       = "Pending"#asource.decode("utf-8") 
                                    dl.ax25Protocol     = "Pending"#protocol.decode("utf-8") 
                                    dl.ax25Control      = "Pending"#control.decode("utf-8") 
                                    dl.packetNumber     = pn[0]
                                    dl.frameTypeId      = frameTypeId 
                                                                
                                    dl.save()
                                    #frameTypeId = unpack("<B",payload[0])
                                    
                                    try:
                                        #Console.log("Packet number: "+str(pn))
                                    
                                        Console.log(str(datetime.datetime.utcnow()) +"-TLM Recv:"+str(pn)+"-"+FrameType.objects.get(pk=frameTypeId).description+"-bytes: "+str(len(data.data)))
                                    except ObjectDoesNotExist:
                                        print("Tipo de telemetria no encontrado")
                                    
                                    telvars = TlmyVarType.objects.filter(satellite__code=satellite).filter(frameType__aid=frameTypeId)
                                    
                                    for tt in telvars:
                                        #TODO
                                        #code draft
                                        if tt.bitsLen >= 8:
                                            bitLen_div =tt.bitsLen // 8
                                            if bitLen_div == 1:
                                                raw = unpack("<B",  payload[tt.position:tt.position+bitLen_div])[0]
                                            else:
                                                raw = unpack("<H",  payload[tt.position:tt.position+bitLen_div])[0]
                                        else:
                                            raw = is_set(payload[tt.position], tt.subPosition)                                         
                                                 
                                        
                                        
                                        tvar                = TlmyVar()
                                        tvar.code           = tt.code
                                        tvar.tlmyVarType    = tt
                                        tvar.setValue(raw, True)
                                        tvar.save()
        
                                        
                                        #tv = tt.setValue(raw, True)
                                        #tv.save()
                                        
                                        
                                        
                                    
                                    #Console.log("Data processed("+str(timezone.datetime.utcnow() )+")")
                                    
                                    data.processed = True
                                    data.processedTime = (timezone.now()-startproctime).total_seconds() 
                                    data.save()
                                ##f.close()
                            except socket.timeout:
                                #Error de timeout de sockets, si el satelite esta en linea 
                                Console.log("Socket timeout", WARNING)
                               
                                
                            """
                            Si el satelite esta en linea debo mandar comandos pendientes
                            """
                            
                            
                            pendingCommands = cmdmgr.getPendingCommands()
                        
                            i = i + 1
                                
                            header = b'\x56'
                            
                            ilen = 0
                            for com in pendingCommands:
                                
                                #Console.log("Se hardcodea ejecucion comando "+str(com.pk))
                                
                                try:
                                
                                    prepack = asource+destination+control+protocol+unhexlify(com.commandType.commandCode)
                                    
                                    
                                    
                                    for p in com.parameters.all():
                                       
                                        #prepack += unhexlify(p.value.zfill(2))
                                        v = bytes([(int(p.value))])
                                        prepack += v
                                        #print(p.value)
                                    
                                    #El byte de inicio \x56 + 4 bytes del entero que indica el tamanio + el tamanio del paquete
                                    ilen = 1+4+len(prepack)
                                    #Mucha atencion con <I, big endian / little endian
                                    prepackpluslen = header+pack('<I', ilen)+prepack
                                    s.send(prepackpluslen)
                                    
                                    
                                    
                                    Console.log("Comando "+str(com.commandType.commandCode)+" enviado")
                                    
                                    
                                    com.setExecuted()
                                    #TODO: Encodear y mandar al satelite por el mismo socket aca!
                                except:
                                    com.setFailed()
                                    
                            
                            
                    finally:
                        s.close()
                        
                
                except Exception as err:
                    Log.create("ERROR TlmyCmdProcessor", "Error/Exception "+str(err), module, Log.ERROR).save()
                    #TODO, quitar print
                   
                    Console.log(err.__str__(), WARNING)
                    
                    unconnectionLimit = unconnectionLimit + 1
                     
                except IOError as err2:
                    Log.create("IOERROR TlmyCmdProcessor", "Error/Exception "+str(err2), module, Log.ERROR).save()
                    #TODO, quitar print
                    Console.log(err2.__str__(), WARNING)
                    unconnectionLimit = unconnectionLimit + 1
                  
                
                Console.log("Sleeping")
                time.sleep(int(DISCONNECTION_SLEEP))
                    
    except ValueError as ve:
        Log.create("Failed connection..", "Error/Exception "+str(ve), module, Log.ERROR).save()
        print("Failed connection..")
        
    print("Finalized")
    
        
    

        