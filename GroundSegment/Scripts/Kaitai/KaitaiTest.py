'''
Created on 05-nov-2020

@author: pabli
'''
from GroundSegment.celery import loadDjangoApp
import importlib
loadDjangoApp()
from Telemetry.models.TlmyRawData import TlmyRawData

import re
import functools
from Scripts.Kaitai.KaitaiStructs import Bugsat1


FIELD_REGEX = re.compile(
    r':field (?P<field>[\*\w]+): (?P<attribute>.*?)'
    r'(?:(?=:field)|\Z|\n)', re.S)


def get_fields(struct, empty=False):
    """
    Get fields defined in docstring
    """
    fields = {}

    try:
        doc_fields = FIELD_REGEX.findall(struct.__doc__)
    except TypeError:
        return fields

    for key, value in doc_fields:
        try:
            fields[key] = functools.reduce(getattr, value.split('.'), struct)
        except AttributeError:
            if empty:
                fields[key] = None

    return fields


if __name__ == '__main__':
    
    module = importlib.import_module("KaitaiStructs")
    class_ = getattr(module, "Bugsat1")
    
    rds = TlmyRawData.objects.filter(satellite__code="TITA").order_by('-id')[:100];
    
    for rd in rds:
        try:
            instance = class_.from_bytes(rd.getBlob().tobytes())
        except:
            pass
        #decoder_class = getattr(decoder, decoder_name.capitalize())
        #frame = decoder_class.from_bytes(raw_frame)
    
        fields = get_fields(instance)
        
        for key, value in fields.items():
            print(key,"=", value)
            
        print("-----------------------------------------")
    print("Fin de ejecucion")
    
    