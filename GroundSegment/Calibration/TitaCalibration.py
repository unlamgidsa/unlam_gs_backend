from Calibration.BaseCalibration import BaseCalibration
from datetime import datetime, timedelta
#import sys
import importlib
from struct import unpack

#from Telemetry.models.TlmyVar import TlmyVar





class TitaCalibration(BaseCalibration):
    def __init__(self):
        pass
    
    def TITAPktDateTime(self, raw):
        pass
    
    def TITAGetFrameType(self, obj, raw):
        ##beacon id
        if (raw.hex()[32:38] == "fffff0") and (raw.hex()[38:42]=="0001"):
            return 998
        else:
            return None
        
        
    