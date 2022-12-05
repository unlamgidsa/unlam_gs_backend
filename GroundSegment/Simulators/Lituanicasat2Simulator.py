'''
Created on 18 jul. 2018

@author: pablo
'''
import sys
from django.utils.datetime_safe import datetime
import time

#path = __file__

import sys, os
dire = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.db.models import Q
from Utils.PktsHelpers import sendJsonDataPkt
from Telemetry.models.TlmyRawData import TlmyRawData
from GroundSegment.settings import APIURL

if __name__ == '__main__':
    

    while(True):
        tlmyRawData = TlmyRawData.objects.filter(~Q(tag="SIMULATION"),satellite__code="LITUANICASAT2").order_by('pktdatetime')
        for rawpkt in tlmyRawData:
            #Para que la simulacion se completa se debe insertar el paquete por el servicio http
            try:
                pktdt = datetime.utcnow()
                sendJsonDataPkt(APIURL, pktdt, pktdt, "LITUANICASAT2", rawpkt.strdata, rawpkt.strpayload, False, "SIMULATION")
            except:
                print("Fallo envio pero sigo intentando")    
            print("Sleeping")
            time.sleep(5)