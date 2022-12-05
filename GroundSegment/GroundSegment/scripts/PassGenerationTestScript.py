'''
Created on Mar 13, 2017

@author: ubuntumate
'''


import os, sys


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.utils import timezone
from datetime import timedelta

from GroundSegment.models.Sitio import Sitio
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.PassGeneration import PassGeneration


if __name__ == '__main__':
    
    
    from GroundSegment.models.Pasada import Pasada
    for p in Pasada.objects.all():
        p.delete()
    
    from GroundSegment.models.PassGeneration import PassGeneration
    for pg in PassGeneration.objects.all():
        pg.delete()
    
    #for p in Pasada.objects.all():
    #    p.delete()
    





    for pg in PassGeneration.objects.all():
        pg.delete()
    
    
    
    sitio = Sitio.objects.get(name="ETC")
    sat = Satellite.objects.get(code="ISS")
    
    afrom = timezone.now()
    ato = afrom+timedelta(days=5)
    
    sitio.getPasses(sat, afrom, ato)
    
    print("FIN")