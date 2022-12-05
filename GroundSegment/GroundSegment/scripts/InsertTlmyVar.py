import struct
import requests
from rest_framework import status
from GroundSegment.Utils.PktsHelpers import sendJsonDataPkt
from GroundSegment.GroundSegment.settings import APIURL
from datetime import datetime
import sys
import time
from GroundSegment import config


sys.path.insert(0, '../GroundSegment')
sys.path.insert(0, '../GroundSegment/Utils')
#from binascii import unhexlify
# It have to be a run function to work with python manage.py runscript SignalsAddTlmyVar
# __init__ file is also needed
# python manage.py runscript SignalsAddTlmyVar
# Finally django access was not needed

if __name__ == '__main__':
    # Parece no funcionar si es proceso aparte, se desarrolla acceso via webservice
    """
    from Telemetry.models.TlmyVar import TlmyVar
    from GroundSegment.models.Satellite import Satellite
    sat = Satellite.objects.get(code="RTEmuSat")
    vt = sat.tmlyVarType.all()
    TlmyVar.objects.filter(tlmyVarType__in=vt)
    """

    user = config.GS_API_USER
    password = config.GS_API_PASSWORD
    sendsession = requests.Session()
    # TODO replace with values from db.
    sendsession.auth = (user, password)
    sendsession.headers.update(
        {'Accept': 'application/json', 'Content-Type': 'application/json', })

    for i in range(100):
        try:
            chunk = struct.pack("<h", i)
            dtn = datetime.utcnow()
            res = sendJsonDataPkt(APIURL,
                                  dtn,  # captureddt
                                  dtn,  # packet
                                  "12000",
                                  chunk.hex(),
                                  chunk.hex(),
                                  True,
                                  "EMU",
                                  sendsession)

            if res.status_code == status.HTTP_409_CONFLICT:
                print("Duplicated", res)

            elif res.status_code == status.HTTP_201_CREATED:
                print("Created", res)

            else:
                print("Packet isn't accepted", res)

        except Exception as e:
            print("Exception sending data to rest service ", e)
            # else:
        time.sleep(1)
    print("Fin ejecución")

    """
    sat = Satellite.objects.get(code="RTEmuSat")
    varTypes = sat.tmlyVarType.all()
   
    TlmyVar.objects.filter(tlmyVarType__in=varTypes).delete()
 
    for i in range(10000):
        utcdt   = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        newVar = TlmyVar.create(telemetry_type=TlmyVarType.objects.get(code="Var1"),
                                    value=25.5,
                                    tstamp=utcdt)
        time.sleep(3);           
        newVar.save()
        print("Nueva variable salvada")
        
    print("Fin de script")
    """
