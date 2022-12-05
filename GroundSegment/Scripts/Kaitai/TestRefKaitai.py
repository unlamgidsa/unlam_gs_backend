'''
Created on 17 jun. 2020

@author: pablo
'''

from GroundSegment.celery import loadDjangoApp

loadDjangoApp()
from Telemetry.models.TlmyRawData import TlmyRawData


import importlib
if __name__ == '__main__':
    
    module = importlib.import_module("KaitaiStructs")
    class_ = getattr(module, "Bugsat1")

    rd = TlmyRawData.objects.filter(satellite__code="TITA").last();
    instance = class_.from_bytes(rd.getBlob().tobytes())
    
    for att in dir(instance.ax25_frame.payload.ax25_info.beacon_type):
        
        if(callable(getattr(instance.ax25_frame.payload.ax25_info.beacon_type, att))==True):
            pass
            #Si es callable es una funcion, no me interesa
            
        else:
            #si arranca con _ tampoco me interesa
            if att.startswith('_'):
                pass
            else:
                #En este caso tenemos un atributo..., sino existe el tipo de variable de telemetria se deberia
                #crear, tenemos todo o casi todo para hacerlo, falta la funcion de calibracion.
                #No se puede obtener el byte de la trama y por tanto eso quedaria nulo...
                print (att, getattr(instance.ax25_frame.payload.ax25_info.beacon_type, att), type(att))
    
    #print("Telemetria valor: ", instance.Telemetry.pcm_5v_v);
    
    print("Fin de programa");