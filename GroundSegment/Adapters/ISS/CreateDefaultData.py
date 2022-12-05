'''
Created on 09-abr-2021

@author: pabli
'''
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from Telemetry.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.SubSystem import SubSystem
from Telemetry.models.TlmyVarType import CType, TlmyVarType


def createDefaultData():
  iss, created = Satellite.objects.get_or_create(code="ISS",
                                                 description="International Space Station",
                                                 noradId=25544,
                                                 state=SatelliteState.objects.get(code="NOMINAL"),
                                                 active=True, 
                                                 inContact=False,
                                                 commServerIP="",
                                                 commServerPort="",
                                                 satnogs=False);
                                                 

  """
  for tt in iss.tmlyVarType.all():
    tt.tlmyVars.all().delete()
    
  for tt in iss.tmlyVarType.all():
    tt.delete()
  """
  
                                                 
  INTEGER = 0;
  FLOAT = 1;
  
  eps = SubSystem.objects.get(code="EPS")
  aocs = SubSystem.objects.get(code="AOCS")
  ctypeShortBigEndian = CType.objects.get(code="short big-endian")
  umDiscrete = UnitOfMeasurement.objects.get(code="(D)")
  umVolt = UnitOfMeasurement.objects.get(code="V")
    
  #['S4000001', 'S4000004', 'P4000001', 'P4000004']
  tlv, created = TlmyVarType.objects.get_or_create(code="S4000001",
                                                   description="Photovolatic Control Unit (PVCU) - Solar Array - 1A - Drive Voltage",
                                                   satellite=iss,
                                                   position=0,
                                                   subPosition=0,
                                                   bitsLen=0,
                                                   subsystem=eps,
                                                   unitOfMeasurement=umVolt,
                                                   ctype=ctypeShortBigEndian)
  tlv.save()

  
  tlv, created = TlmyVarType.objects.get_or_create(code="S4000004",
                                                 description="Photovolatic Control Unit (PVCU) - Solar Array - 3B - Drive Voltage",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=umVolt,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  
  tlv, created = TlmyVarType.objects.get_or_create(code="P4000001",
                                                 description="Photovolatic Control Unit (PVCU) - Solar Array - 2A - Drive Voltage",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=umVolt,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  
  tlv, created = TlmyVarType.objects.get_or_create(code="P4000004",
                                                 description="Photovolatic Control Unit (PVCU) - Solar Array - 4A - Drive Voltage",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=umVolt,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  deg, created = UnitOfMeasurement.objects.get_or_create(code='deg', description='degrees')
  
  tlv, created = TlmyVarType.objects.get_or_create(code="S0000001",
                                                 description="Starboard Thermal Radiator Rotating Joint (TRRJ) Position (degrees)",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  tlv, created = TlmyVarType.objects.get_or_create(code="S0000002",
                                                 description="Port Thermal Radiator Rotating Joint (TRRJ) Position (degrees)",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  tlv, created = TlmyVarType.objects.get_or_create(code="S0000003",
                                                 description="Solar Alpha Rotary Joint (SARJ) Starboard Joint Angle Position (degrees)",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  tlv, created = TlmyVarType.objects.get_or_create(code="S0000004",
                                                 description="Solar Alpha Rotary Joint (SARJ) Port Joint Angle Position",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  tlv, created = TlmyVarType.objects.get_or_create(code="S0000005",
                                                 description="Solar Alpha Rotary Joint (SARJ) Port Joint Angle Commanded Positionn",
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
  tlv.save()
  
  
  
  #S0000001  SPARTAN/VVO  Starboard Thermal Radiator Rotating Joint (TRRJ) Position (degrees)  DEG
  #S0000002  SPARTAN/VVO  Port Thermal Radiator Rotating Joint (TRRJ) Position (degrees)  DEG
  #S0000003  SPARTAN/VVO  Solar Alpha Rotary Joint (SARJ) Starboard Joint Angle Position (degrees)  DEG
  #S0000004  SPARTAN/VVO  Solar Alpha Rotary Joint (SARJ) Port Joint Angle Position (degrees)  DEG
  #S0000005  VVO  Solar Alpha Rotary Joint (SARJ) Port Joint Angle Commanded Position (degrees)  DEG

  photovolatic_list = [('P4000007', 'Photovolatic Control Unit (PVCU) - Solar Array - 2A - Beta Gimble Assembly (BGA) Position'),
                       ('P4000008', 'Photovolatic Control Unit (PVCU) - Solar Array - 4A - Beta Gimble Assembly (BGA) Position'),
                       ('P6000007', 'Photovolatic Control Unit (PVCU) - Solar Array - 4B - Beta Gimble Assembly (BGA) Position'),
                       ('P6000008', 'Photovolatic Control Unit (PVCU) - Solar Array - 2B - Beta Gimble Assembly (BGA) Position'),
                       ('S4000007', 'Photovolatic Control Unit (PVCU) - Solar Array - 1A - Beta Gimble Assembly (BGA) Position'),
                       ('S4000008', 'Photovolatic Control Unit (PVCU) - Solar Array - 3A - Beta Gimble Assembly (BGA) Position'),
                       ('S6000007', 'Photovolatic Control Unit (PVCU) - Solar Array - 3B - Beta Gimble Assembly (BGA) Position'),
                       ('S6000008', 'Photovolatic Control Unit (PVCU) - Solar Array - 1B - Beta Gimble Assembly (BGA) Position')
                      ]  
  

  for v in photovolatic_list:
    tlv, created = TlmyVarType.objects.get_or_create(code=v[0],
                                                 description=v[1],
                                                 satellite=iss,
                                                 position=0,
                                                 subPosition=0,
                                                 bitsLen=0,
                                                 subsystem=eps,
                                                 unitOfMeasurement=deg,
                                                 ctype=ctypeShortBigEndian)
    tlv.save()