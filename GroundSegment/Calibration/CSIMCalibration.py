'''
Created on 11-nov-2020

@author: pabli
'''

from Calibration.BaseCalibration import BaseCalibration
from datetime import datetime, timedelta
#import sys
import importlib
from struct import unpack

#from Telemetry.models.TlmyVar import TlmyVar


FRAME_UI272 = 996
FRAME_UI131 = 995
FRAME_I     = 994

class CSIMCalibration(BaseCalibration):

    
    def CSIMPktDateTime(self, obj, raw):
        pass
    
    
    def CSIMGetFrameType(self, obj, raw):
        #ctl = raw.hex()[14] & 0x13 # address 0E
        ctl         = raw[14];#type bytes
        frame_ret   = None
        if (ctl == b'\x03' or ctl == b'\x13') and len(raw) == 272:
            frame_ret = FRAME_UI272
    
        elif (ctl == b'\x03' or ctl == b'\x13') and len(raw) == 131:
            frame_ret = FRAME_UI131
    
        elif (ctl == b'\x00' or ctl == b'\x02' or ctl == b'\x10' or ctl == b'\x12'):
            frame_ret = FRAME_I
    
        return frame_ret
    