'''
Created on Aug 15, 2017

@author: ubuntumate
'''
import unittest

from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.FrameType import FrameType
from GroundSegment.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TlmyVar import TlmyVar
from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.SubSystem import SubSystem
from GroundSegment.models.Coefficient import Coefficient
import random
import datetime

class Test(unittest.TestCase):


    def setUp(self):
        self.cantVars = 5000
        self.iterations = 15


    def tearDown(self):
        pass

    def test01SatelliteState(self):
        print("test..2...")
        st1 = SatelliteState()
        st1.code = "Nominal"
        st1.description = "Nominal"
        st1.save()

    def test02Satellite(self):
        
        try:
            st = SatelliteState.objects.first()
            sat = Satellite.new("FS2017", "Satelite Formador 2017", 98745, st)
            sat.save()
        except:
            pass


    def test03FrameType(self):
        frame_type = FrameType()
        frame_type.aid = 1
        frame_type.description = "AllTelemetry"
        frame_type.save()


    def test04UnitOfMeasurement(self):
        unit_M = UnitOfMeasurement()
        unit_M.code = "C"
        unit_M.description = "Grados Celcius"
        unit_M.save()

        
        
    def test05SubSystem(self):
           
        s = SubSystem()
        s.code = "GENERIC"
        s.description = "GENERIC"
        s.save()

    def test10LinealCalibration(self):
        lc = Calibration()
        lc.aClass = "GCalibration"
        lc.aMethod = "linealCalibration"
        lc.subsystem = SubSystem.objects.get(code="GENERIC")
        lc.save()
        
        
        lc = Calibration()
        lc.aClass = "GCalibration"
        lc.aMethod = "resetCauseCalibration"
        lc.subsystem = SubSystem.objects.get(code="GENERIC")
        lc.save()
        
        

    def test11Create5000Vars(self):
        print("Creando", self.cantVars, "variables de telemetria")
        
        cm1 = Calibration.objects.get(aClass = "GCalibration", aMethod = "linealCalibration")
        cm2 = Calibration.objects.get(aClass = "GCalibration", aMethod = "resetCauseCalibration")
        
        
        tvrs = []
        for i in range(0, self.cantVars):
            tlmy_varType = TlmyVarType()
            tlmy_varType.code = "VT"+str(i)
            tlmy_varType.description = "VT"+str(i)
            sat = Satellite.objects.first()
            tlmy_varType.satellite = sat 
            tlmy_varType.limitMaxValue = 999.999
            tlmy_varType.limitMinValue = -999.999
            tlmy_varType.maxValue = 999.999
            tlmy_varType.minValue = -999.999
            tlmy_varType.frameType = FrameType.objects.first()
            
            if random.randrange(0, 2)==1:
                tlmy_varType.calibrationMethod = cm1
                tlmy_varType.varType = 1
            
            else:
                tlmy_varType.calibrationMethod = cm2
                tlmy_varType.varType = 2
            
            
            tlmy_varType.save()
            
            c1 = Coefficient()
            c1.code = "GAIN"
            c1.value = 0.5
            c1.tlmyVarType = tlmy_varType
            c1.save()
            
            c2 = Coefficient()
            c2.code = "OFFSET"
            c2.value = 0.5
            c2.tlmyVarType = tlmy_varType
            c2.save()
            

            
        
        print("todas las vars guardada", self.cantVars)    
        
        self.assertEqual(TlmyVarType.objects.count(), self.cantVars, "La cantidad de variables de telemetria a testear no es correcta")

    
    def test12Update5000Vars(self):
        
        
        print("Actualizando las", self.cantVars)
        totaltime = 0
        
        tvts = TlmyVarType.objects.all().prefetch_related("coefficients").select_related("calibrationMethod")
        
        iteration = 0
            
        for i in range(0,self.iterations):
            start = datetime.datetime.utcnow()
            
            tls = []
            iteration += 1
                
            for tv in tvts:
                newvalue = 0
                if (random.randrange(0, 20)==10) or (iteration==1):
                    newvalue = random.randrange(0,20)
                else:
                    newvalue = tv.lastRawValue
                t = TlmyVar()
                t.tlmyVarType = tv
                t.setValue(newvalue)
                tls.append(t)
                    #print(tv.getValue())
                
            
            TlmyVar.objects.bulk_create(tls)    
            tt = (datetime.datetime.utcnow()-start).total_seconds()
            print("Tiempo total", i, tt)
       
    
    """
    def test04Telemetry(self):
        tlmy_varType = TlmyVarType()
        tlmy_varType.code = "PATemp"
        tlmy_varType.description = "PATemp fullname"
        sat = Satellite.objects.first()
        tlmy_varType.satellite = sat 
        tlmy_varType.limitMaxValue = 999.999
        tlmy_varType.limitMinValue = -999.999
        tlmy_varType.maxValue = 999.999
        tlmy_varType.minValue = -999.999
        tlmy_varType.varType = 1
        tlmy_varType.frameType = FrameType.objects.first()
        tlmy_varType.save()
    """

    """
    def test05Telemetry(self):
        print("test05Telemetry")
        tlmy_varType = TlmyVarType.objects.get(code="PATemp")
        
        tlmv = TlmyVar()
        
        tlmv.code = tlmy_varType.code
        tlmv.tlmyVarType = tlmy_varType
        
        tlmv.setValue(25)
        tlmv.save()
        
        
        self.assertEqual(tlmy_varType.getValue(), TlmyVar.objects.filter(code="PATemp").order_by('pk').last().getValue(), "El el ultimo valor cargado no coincide con el de tiempo real")
    """

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()