'''
Created on 17 abr. 2019

@author: psoligo
'''

import importlib
import Calibration




def loadDjangoApp():
    import sys; print('%s %s' % (sys.executable or sys.platform, sys.version))
    import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; import django
    from django.core.wsgi import get_wsgi_application
    from attr._compat import isclass
    return get_wsgi_application()


    

#@app.task(bind=True)
def autodiscover(self): 
    

    import os
    import types
    application = loadDjangoApp()  
    
    
    
    import inspect
 
    import Telemetry
    import GroundSegment
    from Calibration.BaseCalibration import BaseCalibration
    from Telemetry.models import Calibration as clb
    
    #print("Base->",cal.BaseCalibration)
    buildin_methods = ['__init__',] 
    
    #importlib.reload(Calibration)
    for name, data in inspect.getmembers(Calibration):
        
        if inspect.isclass(data) and issubclass(data, BaseCalibration) and (name!="BaseCalibration"):
            #print("==>", name, data)
            for mtdName, mdata in inspect.getmembers(data):
                if type(mdata)==types.FunctionType and not mtdName in buildin_methods:
                    #print("\t=>", mtdName)
                    l = clb.Calibration.objects.filter(aClass=name, aMethod=mtdName)
                    if len(l)==0:
                        calmethod           = clb.Calibration()
                        calmethod.aClass    = name
                        calmethod.aMethod   = mtdName
                        calmethod.subsystem = GroundSegment.models.SubSystem.objects.order_by('?').first()
                        calmethod.save()
                        print("NUEVA FUNCION DE CALIBRACION", mtdName)
                    else:
                        print("----SIN NOVEDADES----")
                    
            
        """
        
        
        if(type(data)==types.ModuleType):
            #print("Modulos-->", name, type(data)) 
            importlib.reload(data)
            #Hasta aca modulo, ahora itero el modulo para obtener clases
            for lname, ldata in inspect.getmembers(data):
                
                if(type(ldata)==types.ModuleType.__class__):
                    print("---->",ldata)
                    if issubclass(ldata, Calibration.BaseCalibration.BaseCalibration) and (ldata!=Calibration.BaseCalibration.BaseCalibration):
                        #Aca tengo la clase, que metodos tengo??
                        print("\t\tDentro del modulo", lname, type(ldata))
                        
                        for mtdName, mdata in inspect.getmembers(ldata):
                            if type(mdata)==types.FunctionType:
                                    
                                l = Telemetry.models.Calibration.objects.filter(aClass=lname).filter(aMethod=mtdName)
                                if len(l)==0:
                                    calmethod           = Telemetry.models.Calibration()
                                    calmethod.aClass    = lname
                                    calmethod.aMethod   = mtdName
                                    calmethod.subsystem = GroundSegment.models.SubSystem.objects.order_by('?').first()
                                    calmethod.save()
                                    print("NUEVA FUNCION DE CALIBRACION")
                                else:
                                    print("----SIN NOVEDADES----")
                                    
                                    
        """