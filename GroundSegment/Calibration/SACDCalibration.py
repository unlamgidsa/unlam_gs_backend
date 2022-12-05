'''
Created on 9 may. 2019

@author: psoligo
'''
from Calibration.BaseCalibration import BaseCalibration
from datetime import datetime, timedelta
#import sys
import importlib
from struct import unpack

from dateutil import tz
import pickle
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.tree import DecisionTreeRegressor
#from Telemetry.models.TlmyVar import TlmyVar





class SACDCalib(BaseCalibration):
    
    
        
    def __init__(self):
        #Esto no deberia cargarse cada vez, hay que buscar que los tipos de variables de telemetria
        #no se vuelvan a cargar con cada paquete recibido
        print("SE CARGA MODULO Telemetry.models.TlmyVar")
        self.module_TlmyVar     = importlib.import_module('Telemetry.models.TlmyVar')       
        self.module_TlmyVarType = importlib.import_module('Telemetry.models.TlmyVarType')         
        self.module_TlmyRawData = importlib.import_module('Telemetry.models.TlmyRawData') 
        self.pred1              = None
        
        
    def DerivedTest(self, obj, raw):
        #mclss = getattr(self.module_TlmyVar, 'TlmyVar')
        #val = mclss.objects.count()
        return 1
    
    def inEclipse(self, obj, raw):
        #raw deberia ser epoch!
        mclss = getattr(self.module_TlmyRawData, 'TlmyRawData')
        lraw = mclss.objects.get(pk=raw)
        
        secs = unpack('>I', lraw.getBlob()[100:104])[0]
        basedate = datetime(1980,1,6).replace(tzinfo=tz.tzutc())
        pktdt = basedate+timedelta(seconds=secs)
        result = obj.satellite.inEclipse(pktdt)
        
        if result==True:
            return 1
        else:
            return 0
        
        
    def eclipseElapsedTime(self, obj, raw):
        #raw deberia ser epoch!
        mclss = getattr(self.module_TlmyRawData, 'TlmyRawData')
        lraw = mclss.objects.get(pk=raw)
        
        secs = unpack('>I', lraw.getBlob()[100:104])[0]
        basedate = datetime(1980,1,6).replace(tzinfo=tz.tzutc())
        pktdt = basedate+timedelta(seconds=secs)
        
        return obj.satellite.eclipseElapsedTime(pktdt)
    
    def vBatAveragePredicted(self, obj, raw):
        
        
        mclss = getattr(self.module_TlmyVarType, 'TlmyVarType')
        tvt = mclss.objects.get(satellite=obj.satellite, code="vBatAverage(E)")
            
        if hasattr(tvt, 'tlmyprediction'):
            if tvt.tlmyprediction.type.code=='PolinomialRegresion':            
                poli_reg = PolynomialFeatures(degree = 4)
                if self.pred1 == None:
                    self.pred1 = pickle.loads(tvt.tlmyprediction.data.tobytes())
                
                clsTlmyRawData = getattr(self.module_TlmyRawData, 'TlmyRawData')
                lraw = clsTlmyRawData.objects.get(pk=raw)
                
                tv = lraw.tlmyVars.get(tlmyVarType__code="eclipsedElapsedTime")
                
                value = tv.getValue()
                if value<0:
                    value=0
                return self.pred1.predict(poli_reg.fit_transform([[value]]))[0]
            
            elif tvt.tlmyprediction.type.code=='DecisionTreeRegressor':
                reg = DecisionTreeRegressor()
                if self.pred1 == None:
                    self.pred1 = pickle.loads(tvt.tlmyprediction.data.tobytes())
                
                clsTlmyRawData = getattr(self.module_TlmyRawData, 'TlmyRawData')
                lraw = clsTlmyRawData.objects.get(pk=raw)
                tv = lraw.tlmyVars.get(tlmyVarType__code="eclipsedElapsedTime")
                
                return self.pred1.predict([[tv.getValue()]])[0]
                
                
                
            else:
                return 0.0
        else:
            return 0.0
        
    
    
    def vBatAverageMax(self, obj, raw):
        try:
            mclss = getattr(self.module_TlmyVarType, 'TlmyVarType')
            tvt = mclss.objects.get(satellite=obj.satellite, code="vBatAverage(E)")
            tvt.maxValue = self.vBatAveragePredicted(obj, raw) + (tvt.tlmyprediction.std)
            tvt.save()
            return tvt.maxValue
        except:
            return None
        
        
    
    def vBatAverageMin(self, obj, raw):    
        try:
            mclss = getattr(self.module_TlmyVarType, 'TlmyVarType')
            tvt = mclss.objects.get(satellite=obj.satellite, code="vBatAverage(E)")
            tvt.minValue = self.vBatAveragePredicted(obj, raw) - (tvt.tlmyprediction.std)
            tvt.save()
            return tvt.minValue
        except:
            return None
        