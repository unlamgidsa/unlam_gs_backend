'''
Created on 11 jun. 2018

@author: pablo
'''

import os, sys




proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.utils import timezone
from datetime import timedelta, datetime
#nft.__dict__ = ft.__dict__.copy()



from Telemetry.models.TlmyVarType import TlmyVarType, CType
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.Calibration import Calibration
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from Telemetry.models.FrameType import FrameType
from django.contrib.auth.models import User
if __name__ == '__main__':
    #Primero satelites, solo TITA
    satscodes = ['TITA',] 
    TlmyVarType.objects.using('production').all().delete()
    FrameType.objects.using('production').all().delete()
    User.objects.using('production').all().delete()
    Satellite.objects.using('production').all().delete()
    SatelliteState.objects.using('production').all().delete()
    Calibration.objects.using('production').all().delete()
    SubSystem.objects.using('production').all().delete()
    CType.objects.using('production').all().delete()
    UnitOfMeasurement.objects.using('production').all().delete()
    #Borro telemetria y despues frametype
    
    
    
    
    
    
    objs = User.objects.using('development').all()
    for o in objs:
        if not User.objects.using('production').filter(username=o.username).exists():
            o.save(using='production')
    
    
    sts = SatelliteState.objects.using('development').all()
    for st in sts:
        if not SatelliteState.objects.using('production').filter(code=st.code).exists():
            st.save(using='production')
        
    subs = SubSystem.objects.using('development').all()
    for o in subs:
        if not SubSystem.objects.using('production').filter(code=o.code).exists():
            o.save(using='production')
    
    
    clbs = Calibration.objects.using('development').all()
    for o in clbs:
        if not Calibration.objects.using('production').filter(aClass=o.aClass, aMethod=o.aMethod).exists():
            o.save(using='production')
        
        
    #Todos los ctypes, se puede usar id?
    ctps = CType.objects.using('development').all()
    for o in ctps:
        if not CType.objects.using('production').filter(id=o.id).exists():
            o.save(using='production')
            
    #Unidad de medida
    ctps = CType.objects.using('development').all()
    for o in ctps:
        if not CType.objects.using('production').filter(id=o.id).exists():
            o.save(using='production')
    
    objs = UnitOfMeasurement.objects.using('development').all()
    for o in objs:
        if not UnitOfMeasurement.objects.using('production').filter(id=o.id).exists():
            o.save(using='production')
    
    
    
    sats = Satellite.objects.using('development').filter(code__in=satscodes)
    for sat in sats:
        for tvt in sat.tmlyVarType.all():
            if not Satellite.objects.using('production').filter(pk=sat.pk).exists():
                sat.save(using='production')
            
            if not TlmyVarType.objects.using('production').filter(code=tvt.code).exists():
                if not FrameType.objects.using('production').filter(id=tvt.id).exists():
                    tvt.frameType.save(using='production')
                #Ya esta el frame type
                tvt.save(using='production')
        
 
print("Fin de proceso")
