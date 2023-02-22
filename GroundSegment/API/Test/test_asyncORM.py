'''
Created on Mar 26, 2017

@author: ubuntumate
'''
import unittest
from django.utils.timezone import datetime, now, timedelta
from django.core.exceptions import ObjectDoesNotExist
from Telemetry.models.Calibration import Calibration
from Telemetry.models.Coefficient import Coefficient
from GroundSegment.models.Satellite import Satellite
#from GroundSegment.celery import loadDjangoApp
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from Telemetry.models.FrameType import FrameType
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.SubSystem import SubSystem
from django.db.models import Q


class TestAsync(unittest.TestCase):
    def setUp(self):
        self.sat_code = "SatTest"
        self.__initDataBase__()
        

    def tearDown(self):
        pass
        
    
    def __initDataBase__(self):   
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        if(created):
            ss.save()
        try:
            sat = Satellite.objects.get(code=self.sat_code)
        except Satellite.DoesNotExist as ex:
            sat = Satellite()
            sat.code        = self.sat_code
            sat.description = self.sat_code
            sat.noradId     = 0
            sat.state          = SatelliteState.objects.first()
            sat.inContact      = False
            sat.save()
        
        frameType, created      = FrameType.objects.get_or_create(aid=-9, description="NoFrame", satellite=sat)
        if(created):
            frameType.save()

        um, created             = UnitOfMeasurement.objects.get_or_create(code="N/A", description="N/A")
        if(created):
            um.save()

        subsystem, created      = SubSystem.objects.get_or_create(code="ALL", description="ALL")
        if(created):
            subsystem.save()
        
        CType.createBasics()

        tvts = sat.tmlyVarType.all()
        for tvt in tvts:
            #Si existe el tipo le borro todas las tlmyVars y luego borro el tipo
            tvt.coefficients.all().delete()
            try:
                #tt = sat.tmlyVarType.get(code=frmTvt["name"])
                #Elimino las variables
                tvt.tlmyVars.all().delete()
                #Elimino el tipo
                tvt.delete()
            except TlmyVarType.DoesNotExist:
                print("Telemetria no existente")

        #Elimino los raw del satelite
        sat.rawdatas.all().delete()    
        
        ctypes = CType.objects.filter(code__in=['int little-endian', 'float little-endian', 'string little-endian', 'bool little-endian'])
        #ypes = CType.objects.filter()
        for ctype in ctypes:
            ss, created = TlmyVarType.objects.get_or_create(
                code=ctype.code, #"VT"+ctype.code.split()[0],
                description=ctype.code,
                satellite=sat,
                calibrationMethod=None,
                position=0,
                subPosition=0,
                bitsLen=ctype.length*8,
                unitOfMeasurement=um,
                subsystem=subsystem,
                ctype=ctype
            )
            if created:
                ss.save()

            
        #Agrego una de entera a float con calibracion
        ctype = CType.objects.get(code='float little-endian')
        calib = Calibration.objects.get(aMethod='linealCalibration')
        ss, created = TlmyVarType.objects.get_or_create(
            code=ctype.code+"wpro", #"VT"+ctype.code.split()[0],
            description=ctype.code+"wpro",
            satellite=sat,
            calibrationMethod=calib,
            position=0,
            subPosition=0,
            bitsLen=ctype.length*8,
            unitOfMeasurement=um,
            subsystem=subsystem,
            ctype=ctype
        )
        if created:
            ss.save()
            c1 =  Coefficient(code='GAIN', value=0.5, tlmyVarType=ss)
            c1.save()
            c2 =  Coefficient(code='OFFSET', value=3, tlmyVarType=ss)
            c2.save()
        
            
            #Tienen que existir, dar de alta por script que peine toda las posibilidades
        return sat


    async def test_getAllSatellites(self):
        async for sat in Satellite.objects.aget(code="SatTest"):
            print(sat)
            self.assertEqual(sat.code, "SatTest", "The async function doesn't work")



    async def test_getTlmyVarTypes(self):
        tvtlist = []
        async for tvt in TlmyVarType.objects.aall():
            tvtlist.append(tvt)
        
        self.assertGreater(len(tvtlist), 0, "Error")
        
            



            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCommand']
    unittest.main()