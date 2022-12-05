'''
Created on 12 abr. 2019

@author: psoligo
'''
import sys; print('%s %s' % (sys.executable or sys.platform, sys.version))
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; import django
from django.core.wsgi import get_wsgi_application
from attr._compat import isclass
application = get_wsgi_application()

import os
import types
import importlib
import inspect
import Calibration
from Calibration.BaseCalibration import BaseCalibration
import Telemetry
import GroundSegment
import time
import py_compile

if __name__ == '__main__':
    

    while(1):
       
        cal = importlib.reload(Calibration)
        #print("Base->",cal.BaseCalibration)
         
        for name, data in inspect.getmembers(cal):
            
            if(type(data)==types.ModuleType):
                
                print("Modulos-->", name, type(data)) 
                #Hasta aca modulo, ahora itero el modulo para obtener clases
                importlib.reload(data)
                for lname, ldata in inspect.getmembers(data):
                    if(type(ldata)==types.ModuleType.__class__):
                        
                        if issubclass(ldata, Calibration.BaseCalibration.BaseCalibration) and (ldata!=Calibration.BaseCalibration.BaseCalibration):
                            #Aca tengo la clase, que metodos tengo??
                            print("\t\tDentro del modulo", lname, type(ldata))
                    
                            for mtdName, mdata in inspect.getmembers(ldata):
                                if type(mdata)==types.FunctionType:
                                    print("\t\t\t\tDentro de la clase", mtdName, type(mdata))
                                    l = Telemetry.models.Calibration.objects.filter(aClass=lname).filter(aMethod=mtdName)
                                    if len(l)==0:
                                        calmethod           = Telemetry.models.Calibration()
                                        calmethod.aClass    = lname
                                        calmethod.aMethod   = mtdName
                                        calmethod.subsystem = GroundSegment.models.SubSystem.objects.order_by('?').first()
                                        #calmethod.save()
                                        print("Nueva funcion de calibracion guardada llamada ", mtdName)
                                    else:
                                        print("Todo sigue igual")
                     
                     
        time.sleep(5)
        
    print("Fin!")
