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
import struct
from django.db.models import Q

class Test(unittest.TestCase):
    def setUp(self):
        self.sat_code = "SatTest"
        self.__initDataBase__()
        

    def tearDown(self):
        pass
        
    def test01_assignIntValue(self):
        sat         = Satellite.objects.get(code=self.sat_code)
        value       = 33
        ctypestr    = "int little-endian"
        ctype       = CType.objects.get(code = ctypestr)
        raw                 = struct.pack(ctype.format, value)
        tt                  = sat.tmlyVarType.get(ctype=ctype, calibrationMethod=None)
        tvar                = TlmyVar()
        tvar.code           = tt.code[0:23]
        tvar.tlmyVarType    = tt
        tvar.tlmyRawData    = None
        tvar.setValue(raw, now())
        tvar.save()
        self.assertEqual(tvar.getValue() , value, "Error encode - decode int little-endian")
        

                
        

    def test02_assignFloatValue(self):
        sat         = Satellite.objects.get(code=self.sat_code)
        value = 33.5
        ctypestr            = "float little-endian"
        ctype               = CType.objects.get(code = ctypestr)
        raw                 = struct.pack(ctype.format, value)
        tt                  = sat.tmlyVarType.get(ctype=ctype, calibrationMethod=None)
        tvar                = TlmyVar()
        tvar.code           = tt.code[0:23]
        tvar.tlmyVarType    = tt
        tvar.tlmyRawData    = None
        tvar.setValue(raw, now())
        tvar.save()
        self.assertEqual(tvar.getValue() , value, "Error encode - decode float little-endian")

    def test03_assignStringValue(self):
        sat                 = Satellite.objects.get(code=self.sat_code)
        value               = "TEST"


        ctypestr            = "string little-endian"
        ctype               = CType.objects.get(code = ctypestr)
        
        evalue                = bytes(value, 'utf-8')    # Or other appropriate encoding
        #struct.pack("I%ds" % (len(s),), len(s), s)
        #pack('{}s'.format(len(string)), string)
        #unpack('{}s'.format(len(data)), data)
        raw                 = struct.pack('{}s'.format(len(evalue)), evalue) 
        tt                  = sat.tmlyVarType.get(ctype=ctype, calibrationMethod=None)
        tvar                = TlmyVar()
        tvar.code           = tt.code[0:23]
        tvar.tlmyVarType    = tt
        tvar.tlmyRawData    = None
        tvar.setValue(raw, now())
        tvar.save()
        self.assertEqual(tvar.getValue() , value, "Error encode - decode string little-endian")

    def test04_assignBooleanValue(self):
        pass

    def test05_assignFloatValueWCalibmethod(self):
        sat         = Satellite.objects.get(code=self.sat_code)
        value       = 33
        ctypestr    = "float little-endian"
        ctype       = CType.objects.get(code = ctypestr)
        raw                 = struct.pack(ctype.format, value)
        tt                  = sat.tmlyVarType.filter(~Q(calibrationMethod = None)).get(ctype=ctype)
        tvar                = TlmyVar()
        tvar.code           = tt.code[0:23]
        tvar.tlmyVarType    = tt
        tvar.tlmyRawData    = None
        tvar.setValue(raw, now())
        tvar.save()
        value = value*tt.coefficients.get(code="GAIN").value+tt.coefficients.get(code="OFFSET").value
        self.assertEqual(tvar.getValue() , value, "Error encode - decode float little-endian with method")
    
     
    def test01(self):
        pass
        """
        sat = Satellite.objects.get(code="BDSat")
        tvt = sat.tmlyVarType.get(code="AV2868")
        tv = tvt.tlmyVars.last()
        tv.setPredictedValue("10")
        tv.save()
        self.assertEqual(tv.getPredictedValue() , 10, "No se almaceno valor predicho")
        
        pk = tv.pk
        tv = None
        tv = TlmyVar.objects.get(id=pk)
        self.assertEqual(tv.getPredictedValue() , 10, "No se almaceno valor predicho")
        """

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

            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCommand']
    unittest.main()