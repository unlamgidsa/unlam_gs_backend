'''
Created on 2 de dic. de 2016

@author: pabli
'''
from GroundSegment.models.Parameter import Parameter



def loadOrCreateParam(paramKey, paramModule, paramValue, paramDescription):
    """
    Devuelve el valor de un parametro del configuracion del sistema, en caso de}
    no existir lo crea con un default hardcodeado, esto ultimo tiene como objetivo
    simplificar la primera ejecucion del sistema y ofrecer informacion sobre la naturaleza
    del paremetro en el momento de ser modificado
    """
    """
    Busco el parametro por medio de su clave
    """
    try:
        param = Parameter.objects.get(key=paramKey)
    except Parameter.DoesNotExist:
        param = None
            
    """
    Aun no fue creado el parametro, debo generarlo
    """
    if param==None:
        param = Parameter.create(paramModule, paramKey, paramValue, paramDescription)
        param.save()
       
        
    return param.value
