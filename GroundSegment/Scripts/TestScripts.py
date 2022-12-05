'''
Created on 25 jul. 2018

@author: pablo
'''


import os, sys, time
from _datetime import datetime, timedelta



proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.Satellite import Satellite
from CODS.models import ReferenceSystem
import pytz
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


if __name__ == '__main__':
    
    
    satname = "FS2017"
    sat = Satellite.objects.get(code=satname)
    
    #sat.propagations.all().delete()
    #sat.ephems.all().delete()
    
    #Los tles no los borros para evitar descargas innecesarias
    #sat.tles.all().delete()
    #Anio mes dia
    
    afrom   = datetime(2015,5,28,0,0,0,0, tzinfo=pytz.UTC)
    ato     = datetime(2019,5,29,0,0,0,0, tzinfo=pytz.UTC)
    
    raws = sat.rawdatas.filter(pktdatetime__range=(afrom, ato))
    
    file = open(satname+"raw_tlmy.bin", "wb")
    
    for raw in raws:
        bl = raw.getBlob()
        print("Guardando raw de ", satname, "Len: ", len(bl))
        
        
        if ((satname=="FS2017") and (len(bl)==146)):        
            file.write(bl)
        
    file.close()
    
    
    print("Fin de script")

        
    
        
    