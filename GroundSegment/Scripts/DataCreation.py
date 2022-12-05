'''
Created on 12 jun. 2018

@author: pablo
'''
import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from Telemetry.models.FrameType import FrameType
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.TlmyVarType import CType, TlmyVarType
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.Calibration import Calibration
from Telemetry.models.Coefficient import Coefficient
from CODS.models import ReferenceSystem

from django.core.exceptions import ObjectDoesNotExist


def CreateSatelliteStates():

    try:        
    
        ss = SatelliteState.objects.get(code="NOMINAL")
    except ObjectDoesNotExist:
        ss = SatelliteState()
        ss.code = "NOMINAL"
        ss.description = "NOMINAL"
        ss.save()


def CreateSatellites():        
    
    ss = SatelliteState.objects.get(code="NOMINAL")
    try:
        sat2 = Satellite.objects.get(code="FS2017")
    except ObjectDoesNotExist:
        sat2 = Satellite.new("FS2017", "FS2017", 25546, ss)
    
        sat2.save()

    try:
        sat2 = Satellite.objects.get(code="LITUANICASAT2")
    except ObjectDoesNotExist:
        sat2 = Satellite.new("LITUANICASAT2", "LITUANICASAT2", 42768, ss)
    
        sat2.save()

        
def CreateCTypes():
    
    ct, created = CType.objects.get_or_create(code="signed char", format="b", length=1)
    ct.save()
    ct, created = CType.objects.get_or_create(code="unsigned char", format="B", length=1)
    ct.save()
    ct, created = CType.objects.get_or_create(code="short little-endian", format="<h", length=2)
    ct.save()
    ct, created = CType.objects.get_or_create(code="unsigned short little-endian", format="<H", length=2)
    ct.save()
    ct, created = CType.objects.get_or_create(code="unsigned 32 little-endian", format="<I", length=4)
    ct.save()

    
def CreateFrameTypesFS2017():
    fs2017 = Satellite.objects.get(code="FS2017")
    
    ft, created = FrameType.objects.get_or_create(aid=1, description="AllTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=2, description="antsTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=3, description="EPSTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=4, description="TrxUVTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=5, description="OBCTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=6, description="antSActTelemetry", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=170, description="rawI2Cpacket", satellite=fs2017)
    ft.save()
    
    ft, created = FrameType.objects.get_or_create(aid=999, description="ACADEMIC_FRAME", satellite=fs2017)
    ft.save()

    
def CreateFrameTypesLituanicasat2():
    litu = Satellite.objects.get(code="LITUANICASAT2")
    
    ft, created = FrameType.objects.get_or_create(aid=990, description="AllTelemetry", satellite=litu)
    ft.save()
    
    
def CreateUnitOfMeasure():

    um, created = UnitOfMeasurement.objects.get_or_create(code="V", description="Volts")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="C", description="Celsius")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="F", description="Faren...")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="A", description="Ampere")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="mA", description="Miliampere")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="DateTime", description="DateTime")
    um.save()
    um, created = UnitOfMeasurement.objects.get_or_create(code="CANT", description="Cantidad")
    um.save()
    
    um, created = UnitOfMeasurement.objects.get_or_create(code="mV", description="Millivolts")
    um.save()

    
def CreateSubsystems():
    ss, created = SubSystem.objects.get_or_create(code="AOCS", description="Acttitude and orbit control system")
    ss.save()
    
    ss, created = SubSystem.objects.get_or_create(code="EPS", description="Power control system")
    ss.save()
    
    
def CreateTITATlmyVarTypes():
    
    #ATENCION FALTA EL FRAMETYPE EN TODAS LAS VARIABLES
    tita = Satellite.objects.get(code="TITA")
    eps = SubSystem.objects.get(code="EPS")
    aocs = SubSystem.objects.get(code="AOCS")
    ctypeShortBigEndian = CType.objects.get(code="short big-endian")
    umDiscrete = UnitOfMeasurement.objects.get(code="(D)")
    umVolt = UnitOfMeasurement.objects.get(code="V")
    umMilliVolt, created = UnitOfMeasurement.objects.get_or_create(code="mV", description="millivolts")
    umMilliVolt.save()
    umAmp = UnitOfMeasurement.objects.get(code="A")
    umRadSec, created = UnitOfMeasurement.objects.get_or_create(code="RS", description="Radianes Segundo")
    umRadSec.save()
    
    INTEGER = 0;
    FLOAT = 1;
    
    linealCalibration = Calibration.objects.get(aClass="GCalibration", aMethod="linealCalibration");
    
    tlv, created = TlmyVarType.objects.get_or_create(code="LowVoltageCounter",
                                                     description="LowVoltageCounter",
                                                     satellite=tita,
                                                     varType=INTEGER,
                                                     position=36 + 16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umDiscrete,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="niceBatterymV",
                                                     description="niceBatterymV",
                                                     satellite=tita,
                                                     varType=INTEGER,
                                                     position=38 + 16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umMilliVolt,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="rawBatteryMv",
                                                     description="rawBatteryMv",
                                                     satellite=tita,
                                                     varType=INTEGER,
                                                     position=40 + 16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umMilliVolt,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="battery_A",
                                                     description="battery_A",
                                                     satellite=tita,
                                                     varType=FLOAT,
                                                     position=42 + 16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umAmp,
                                                     calibrationMethod=linealCalibration,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    if created:
        coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                         value=0.005237,
                                                         tlmyVarType=tlv)
        coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                         value=0.0,
                                                         tlmyVarType=tlv)
    
    #----------------------------------------------------------------------------
    """
    tlv, created = TlmyVarType.objects.get_or_create(code="pcm_3v3_V", 
                                                     description="pcm_3v3_V", 
                                                     satellite=tita,
                                                     varType=FLOAT,
                                                     position=44+16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umVolt,
                                                     calibrationMethod=linealCalibration,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    if created:
        coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                         value=0.003988,
                                                         tlmyVarType=tlv)
        coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                         value=0.0,
                                                         tlmyVarType=tlv)
        
    #----------------------------------------------------------------------------
    tlv, created = TlmyVarType.objects.get_or_create(code="pcm_3v3_A", 
                                                     description="pcm_3v3_A", 
                                                     satellite=tita,
                                                     varType=FLOAT,
                                                     position=46+16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umAmp,
                                                     calibrationMethod=linealCalibration,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    if created:
        coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                         value=0.005237,
                                                         tlmyVarType=tlv)
        coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                         value=0.0,
                                                         tlmyVarType=tlv)
        
    #----------------------------------------------------------------------------
    tlv, created = TlmyVarType.objects.get_or_create(code="pcm_5v_V", 
                                                     description="pcm_5v_V", 
                                                     satellite=tita,
                                                     varType=FLOAT,
                                                     position=48+16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umVolt,
                                                     calibrationMethod=linealCalibration,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    if created:
        coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                         value=0.005865,
                                                         tlmyVarType=tlv)
        coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                         value=0.0,
                                                         tlmyVarType=tlv)
        
    #----------------------------------------------------------------------------
    tlv, created = TlmyVarType.objects.get_or_create(code="pcm_5v_A", 
                                                     description="pcm_5v_A", 
                                                     satellite=tita,
                                                     varType=FLOAT,
                                                     position=50+16,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     subsystem=eps,
                                                     unitOfMeasurement=umAmp,
                                                     calibrationMethod=linealCalibration,
                                                     ctype=ctypeShortBigEndian)
    tlv.save()
    if created:
        coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                         value=0.005237,
                                                         tlmyVarType=tlv)
        coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                         value=0.0,
                                                         tlmyVarType=tlv)
    """    
    
    #----------------------------------------------------------------------------
    position_base = 96
    for i in range(1, 5):
    
        lcode = "wheel_" + str(i) + "_radsec"
        tlv, created = TlmyVarType.objects.get_or_create(code=lcode,
                                                         description=lcode,
                                                         satellite=tita,
                                                         varType=FLOAT,
                                                         position=position_base + 16,
                                                         subPosition=0,
                                                         bitsLen=16,
                                                         subsystem=aocs,
                                                         unitOfMeasurement=umRadSec,
                                                         calibrationMethod=linealCalibration,
                                                         ctype=ctypeShortBigEndian)
        tlv.save()
        if created:
            coe, created = Coefficient.objects.get_or_create(code="GAIN",
                                                             value=0.3,
                                                             tlmyVarType=tlv)
            coe, created = Coefficient.objects.get_or_create(code="OFFSET",
                                                             value=0.0,
                                                             tlmyVarType=tlv)
        
        position_base = position_base + 2
    

def CreateLituanicasatTlmyVarTypes():
    
    lituanicasat2 = Satellite.objects.get(code="LITUANICASAT2")
    
    ft = lituanicasat2.framesTypes.get(description="AllTelemetry")
    
    # "V" "C" "F" "A" "mA" "DateTime" "CANT"   
    tlv, created = TlmyVarType.objects.get_or_create(code="OBCMCUTemperature",
                                                     description="OBC MCU Temperature",
                                                     satellite=lituanicasat2,
                                                     position=22,
                                                     subPosition=0,
                                                     bitsLen=8,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=2),
                                                     ctype=CType.objects.get(pk=1),
                                                     frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="OBCHeater0Temperature",
                                                     description="OBC Heater[0] temperature",
                                                     satellite=lituanicasat2,
                                                     position=26,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=2),
                                                     ctype=CType.objects.get(pk=3),
                                                     frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="OBCHeater1Temperature",
                                                     description="OBC Heater[1] temperature",
                                                     satellite=lituanicasat2,
                                                     position=32,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=2),
                                                     ctype=CType.objects.get(pk=3),
                                                     frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="COMMTranceiverTemp",
                                                     description="COMM Tranceiver temperature",
                                                     satellite=lituanicasat2,
                                                     position=54,
                                                     subPosition=0,
                                                     bitsLen=8,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=2),
                                                     ctype=CType.objects.get(pk=1), frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="COMMModeSettings",
                                                     description="COMM Mode settings",
                                                     satellite=lituanicasat2,
                                                     position=55,
                                                     subPosition=0,
                                                     bitsLen=8,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=6),
                                                     ctype=CType.objects.get(pk=2), frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="COMMTransmissionCounter",
                                                     description="COMM Transmission counter",
                                                     satellite=lituanicasat2,
                                                     position=60,
                                                     subPosition=0,
                                                     bitsLen=16,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=7),
                                                     ctype=CType.objects.get(pk=4), frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="ADCSStatusMode",
                                                     description="ADCS status mode",
                                                     satellite=lituanicasat2,
                                                     position=87,
                                                     subPosition=0,
                                                     bitsLen=8,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=6),
                                                     ctype=CType.objects.get(pk=2), frameType=ft)
    tlv.save()
    
    tlv, created = TlmyVarType.objects.get_or_create(code="ADCSCurrentTime",
                                                     description="ADCS currentTime",
                                                     satellite=lituanicasat2,
                                                     position=83,
                                                     subPosition=0,
                                                     bitsLen=32,
                                                     unitOfMeasurement=UnitOfMeasurement.objects.get(pk=6),
                                                     ctype=CType.objects.get(pk=5), frameType=ft)
    tlv.save()


def CreateReferenceSystems():
    
    rs, created = ReferenceSystem.objects.get_or_create(code="TOD", description="True of date")
    rs.save()
    
    rs, created = ReferenceSystem.objects.get_or_create(code="MJ2K", description="MJ2000")
    rs.save()
    
    rs, created = ReferenceSystem.objects.get_or_create(code="ICRS", description="International Celestial Reference System")
    rs.save()
    
    rs, created = ReferenceSystem.objects.get_or_create(code="TEME", description="True Equator Mean Equinox")
    rs.save()


def DataCreation():
    """       
    CreateSatelliteStates()
    CreateSatellites()
    CreateCTypes()
    CreateFrameTypesFS2017() 
    CreateFrameTypesLituanicasat2()
    CreateUnitOfMeasure()
    CreateSubsystems()
    CreateLituanicasatTlmyVarTypes()
    CreateReferenceSystems()
    """
    CreateTITATlmyVarTypes()

    
if __name__ == '__main__':
    DataCreation()
    
    print("Fin de script")
    
