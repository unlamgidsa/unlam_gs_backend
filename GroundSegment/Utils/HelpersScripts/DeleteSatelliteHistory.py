'''
Created on 3 dic. 2018

@author: freddie
'''

import os, sys, time
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVar import TlmyVar


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


if __name__ == '__main__':
    
    
    #TlmyRawData.objects.filter(source="TITA", state=TlmyRawData.PROCESSED).update(state=TlmyRawData.PENDING)
    
    TlmyRawData.objects.filter(source="TITA", state=TlmyRawData.PROCESSED).delete()
    TlmyVar.objects.filter(tlmyVarType__satellite__code="TITA").delete()