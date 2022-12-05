'''
Created on 6 jun. 2018

@author: pablo
'''

from Calibration.BaseCalibration import BaseCalibration
from datetime import datetime, timedelta
import struct


class Lituanicasat_Calibration(BaseCalibration):
    
    
    
    
    
    def LituGetFrameType(self, obj, raw):
        ##beacon id
        if len(raw)>200:
            return 997
        else:
            return None

    
    def UTCUnixTimeStamp(self, obj, raw):
        """
        seconds since Jan 01 1970. (UTC) not counting leap seconds.
        Eg: 1495012896
        """
        basedate = datetime(1970,1,1)
        delta = timedelta(seconds=raw)
        return (basedate+delta).__str__()
    
    def LituGetDateTime(self, obj, raw):
        offset = 21
        basedate = datetime(1970,1,1)
        buff = raw[104-offset:104-offset+4]
    
        delta = timedelta(seconds=struct.unpack("<I", buff)[0])
        
        return basedate+delta
    
    
        
        
        
    
    def COMMModeSetting(self, obj, raw):
        if raw==0:
            return "NOT INIT"
        elif raw==1:
            return "SLEEP"
        elif raw==2:
            return "IDLE"
        elif raw==3:
            return "RX"
        elif raw==4:
            return "TX"
        elif raw==5:
            return "CONTINOUS_TX"
        else:
            return "CALIBRATION ERROR"


    def ADCSStatusMode(self, obj, raw):
        if raw==0:
            return "ADCS_INITIAL"
        elif raw==1:
            return "ADCS_DIAGNOSTICS"
        elif raw==2:
            return "ADCS_IDLE"
        elif raw==3:
            return "ADCS_LOG"
        elif raw==4:
            return "ADCS_DETUMBLING"
        elif raw==5:
            return "ADCS_NORMAL"
        elif raw==6:
            return "ADCS_POINTING"
        elif raw==7:
            return "ADCS_PROPULSION"
        elif raw==8:
            return "ADCS_INITIAL_LAUNCH_LOG"
        elif raw==9:
            return "ADCS_CALIBRATION"
        else:
            return "CALIBRATION ERROR"
        
        
