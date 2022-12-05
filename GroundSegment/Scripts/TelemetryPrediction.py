'''
Created on 13 jun. 2019

@author: psoligo
'''

import os, sys, time
from types import FrameType
from datetime import datetime
import time


import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import pytz
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.tree import DecisionTreeRegressor
from struct import unpack
from matplotlib.pyplot import step
from _datetime import timedelta


proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry.models.TlmyPrediction import TlmyPrediction, PredictionType
from Telemetry.models.TlmyRawData import TlmyRawData
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar
from CODS.models import Ephemeride


def regenerateEclipseElapsedTime():
    
    Ephemeride.objects.all().delete()
    
    sat = Satellite.objects.get(code="SACD")
    tt = sat.tmlyVarType.get(code="eclipsedElapsedTime")
    tt.tlmyVars.all().delete()
    tlvsl = []
    
    print("Raw datas del sat", sat.rawdatas.count())
        
        
    raws = sat.rawdatas.order_by('pktdatetime').all()
    cant = raws.count()
    for rd in raws:
        payload             = rd.getPayloadBlob()
        tvar                = TlmyVar()
        tvar.code           = tt.code
        tvar.tlmyVarType    = tt
        tvar.tlmyRawData    = rd
        #raw = unpack(tt.ctype.format,  payload[tt.position:tt.position+tt.ctype.length])[0]
        tvar.setValue(rd.id, rd.pktdatetime)
        tlvsl.append(tvar)
        if len(tlvsl)%500==0:
            print('Regenerando eclipses', len(tlvsl), " de ", cant)
            TlmyVar.objects.bulk_create(tlvsl)
            tlvsl.clear()
            
        
    TlmyVar.objects.bulk_create(tlvsl)   
    print("Finalizada la regeneracion de EET")
    
    

def generateData():
    
    
    sat = Satellite.objects.get(code="SACD")
    try:
        df = pd.read_csv("./Scripts/training.csv")
        
    except:
        #2015-05-29 06:13:35.000Z
        #2015-05-29 07:45:35.000Z
        print("Regenerando datos")
        stepoch = datetime(2015,5,27,10,30,0,0, tzinfo=pytz.UTC)
        enepoch = (stepoch + timedelta(hours=12))
        #enepoch = datetime(2015,5,28,10,30,0,0, tzinfo=pytz.UTC)
        
        #stepoch = datetime(2015,5,27,16,43,0,0, tzinfo=pytz.UTC)
        #enepoch = datetime(2015,5,28,16,43,0,0, tzinfo=pytz.UTC)
        
        
        raws = TlmyRawData.objects.filter(pktdatetime__range=(stepoch, enepoch), satellite=sat).order_by('pktdatetime').select_related('satellite');
        df = pd.DataFrame(columns=['epoch','satellite', 'vBatAverage', 'elapsedEclipseTime'])
        i = 0
        for raw in raws.all():
            epoch                   = raw.pktdatetime
            vBatAverage             = (raw.tlmyVars.get(code="vBatAverage(E)").getValue())
            elapsedEclipseTime      = (raw.tlmyVars.get(code="eclipsedElapsedTime").getValue()) 
            sat                     = raw.satellite.code
            df.loc[epoch] = pd.Series({'epoch':epoch, 'satellite':sat, 'vBatAverage':vBatAverage, 'elapsedEclipseTime':elapsedEclipseTime})
            if i%100==0:
                print("Generando entrenamiento, epoch, ", epoch)
            i+=1
            
        df.to_csv('./Scripts/training.csv')
        df = pd.read_csv("./Scripts/training.csv")
    
    return df

def PolinomialRegressionModel():
    start =  time.time()  
    df = generateData()

    pt, created = PredictionType.objects.get_or_create(code='PolinomialRegresion', description='PolinomialRegresion', aClass="linear_model.LinearRegression")
    pt.save()
    
    
    tvt = TlmyVarType.objects.get(code="vBatAverage(E)")
    df['elapsedEclipseTime'] =   list(map(lambda elapsedEclipseTime: 0 if (elapsedEclipseTime < 0) else elapsedEclipseTime, df['elapsedEclipseTime'])) 
    #df = pd.read_csv("training.csv")
    X = df.iloc[:, 4:5].values
    y = df.iloc[:, 3].values 
    
    #plt.scatter(X, y)
    #plt.show()
    
    
    #Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X, y, test_size=0.2)
    poli_reg = PolynomialFeatures(degree = 4)
    
    X_train_poli = poli_reg.fit_transform(X_train_p)
    X_test_poli = poli_reg.fit_transform(X_test_p) 
    
    #Defino el algoritmo a utilizar
    pr = linear_model.LinearRegression()
    #Entreno el modelo
    pr.fit(X_train_poli, y_train_p)
    
    Y_pred_pr = pr.predict(X_test_poli)
        
    #Y_pred_pr = pr.predict(poli_reg.fit_transform([[800]]))
    #Y_pred_pr
    
    #plt.scatter(X_test_p, y_test_p)
    #plt.plot(X_test_p, Y_pred_pr, color='red', linewidth=3)
    #plt.show()
        
        
    print('PrecisiÃ³n del modelo:')
    print(pr.score(X_train_poli, y_train_p))
    
    import pickle
    
    s = pickle.dumps(pr)
    type(s)
    dt = datetime.utcnow().replace(tzinfo=pytz.UTC)
    if not hasattr(tvt, 'tlmyprediction'):
        dt = datetime.utcnow().replace(tzinfo=pytz.UTC)
        tvt.tlmyprediction = TlmyPrediction(tlmyVarType=tvt, type=pt, updated=dt, expiration=dt, data=s)
        
    else:
        tvt.tlmyprediction.delete()
        tvt.tlmyprediction = TlmyPrediction(tlmyVarType=tvt, type=pt, updated=dt, expiration=dt, data=s)
        """
        if tvt.tlmyprediction.type==pt:
            tvt.tlmyprediction.setData(s)
        else:
            tvt.tlmyprediction.delete()
            tvt.tlmyprediction = TlmyPrediction(tlmyVarType=tvt, type=pt, updated=dt, expiration=dt, data=s)
        """
    tvt.tlmyprediction.genTime =  (time.time()-start)     
    tvt.tlmyprediction.std = df.loc[:,"vBatAverage"].std()
    tvt.tlmyprediction.save()
   
    #pr = pickle.loads(tp.data.tobytes())
    
def DecisionTreeRegressorModel():
    start =  time.time()  
    df = generateData()

    #todos los negativos pasan a ser 0...
    

    pt, created = PredictionType.objects.get_or_create(code='DecisionTreeRegressor', description='DecisionTreeRegressor', aClass="DecisionTreeRegressor")
    pt.save()
    
     
    #df['dis_ec'] =   df['elapsedEclipseTime']//10
    
    
    df['dis_ec'] =   list(map(lambda elapsedEclipseTime: 0 if (elapsedEclipseTime < 0) else elapsedEclipseTime, df['elapsedEclipseTime'])) 
    
    X = np.array(df['dis_ec'])
    epoch = np.array(df['epoch'])
    
    y = np.array(df['vBatAverage'])
    X = X.reshape(-1, 1)
    
    enc = KBinsDiscretizer(n_bins=2, encode='onehot')
    X_binned = enc.fit_transform(X)
    reg = DecisionTreeRegressor(min_samples_split=3, random_state=0).fit(X, y)
    #TODO Analizar presicion del modelo con el tree  
    #print('PrecisiÃ³n del modelo:')
    #print(reg.score(X_train_poli, y_train_p))
    tvt = TlmyVarType.objects.get(code="vBatAverage(E)")
    import pickle
    
    s = pickle.dumps(reg)
    type(s)
    dt = datetime.utcnow().replace(tzinfo=pytz.UTC)
    if not hasattr(tvt, 'tlmyprediction'):
        
        tvt.tlmyprediction = TlmyPrediction(tlmyVarType=tvt, type=pt, updated=dt, expiration=dt, data=s)
        
    else:
        #es el mismo tipo de prediccion?
        if tvt.tlmyprediction.type==pt:
            tvt.tlmyprediction.setData(s)
        else:
            tvt.tlmyprediction.delete()
            tvt.tlmyprediction = TlmyPrediction(tlmyVarType=tvt, type=pt, updated=dt, expiration=dt, data=s)
        
        
        
    tvt.tlmyprediction.genTime =  (time.time()-start)     
    tvt.tlmyprediction.std = df.loc[:,"vBatAverage"].std()
    tvt.tlmyprediction.save()
    #pr = pickle.loads(tp.data.tobytes())
    
    
    
    
    
def TestPlot():
    tlvsl = []
    preds = []
    reals = []
    epochs = []
    print("Generando")
    sc = SACDCalib()
    sat = Satellite.objects.get(code="SACD")
    tvt = TlmyVarType.objects.get(code="vBatAverage(E)")
    raws = sat.rawdatas.all().order_by('pktdatetime')[:1000]
    
    i = 0
    for r in raws:
        
        preds.append(sc.vBatAveragePredicted(tvt, r.id))
        reals.append(r.tlmyVars.get(code="vBatAverage(E)").getValue())
        epochs.append(r.tlmyVars.get(code="vBatAverage(E)").tstamp)
        if i%100==0:
            print("Calculando ",i, " de 8000, vals ->", preds[:-1], reals[:-1] )
        i=i+1
        
    
    print("Finalizada la regeneracion de EET")
        
        
    print("Ploteando")
    plt.plot(epochs, preds, 'y')
    plt.plot(epochs, reals, 'r')
    plt.show()
   

def plotFinalResult():
    
    x = ['RegresiÃ³n Polinomial', 'Ã�rbol de regresiÃ³n']
    y = [92.97, 83.79]
    
    fig, ax = plt.subplots()
    ax.set_ylabel('Segundos')
    ax.bar(x, y, width=0.5, color='r', align='center')
    plt.show()
    
    
    xm = np.arange(0,100)
    #varsPoli = TlmyVar.objects.filter(tlmyVarType__code="vBatAveragePredicted").order_by('tstamp')[:2000].values_list('genTime',flat=True)
    #varsTree = TlmyVar.objects.filter(tlmyVarType__code="vBatAveragePredicted").order_by('tstamp')[:2000].values_list('genTime',flat=True)
    varsPoli = np.loadtxt("./Scripts/varsPoli")[250:350]
    varsTree = np.loadtxt("./Scripts/varsTree")[250:350]
    
    df=pd.DataFrame({'x': xm, 'varsPoli': varsPoli, 'varsTree': varsTree })
    plt.plot( 'x', 'varsPoli', data=df, marker='o', markerfacecolor='skyblue', markersize=5, color='blue', linewidth=4, label="RegresiÃ³n PolinÃ³mica")
    plt.plot( 'x', 'varsTree', data=df, marker='o', markerfacecolor='indianred', markersize=5, color='red', linewidth=4, label="Ã�rbol de regresiÃ³n")

    
    plt.legend()
    plt.show()



if __name__ == '__main__':
    
    #regenerateEclipseElapsedTime()
    
    from Calibration.SACDCalibration import SACDCalib
    from Telemetry.models.TlmyVarType import TlmyVarType
    from Telemetry.models.TlmyRawData import TlmyRawData
    from GroundSegment.models.Satellite import Satellite
    
    #regenerateEclipseElapsedTime()
    #PolinomialRegressionModel()
    #DecisionTreeRegressorModel()

    #plotFinalResult()
    
    
    TaskRegenerateTlmyVar(TlmyVarType.objects.get(code="vBatAveragePredicted").pk)
    #TaskRegenerateTlmyVar(TlmyVarType.objects.get(code="vBatAverageMax").pk)
    #TaskRegenerateTlmyVar(TlmyVarType.objects.get(code="vBatAverageMin").pk)

    print("Fin")
    
    
    
    
    #TestPlot()
    
    
    
    #data set, seria algo asi
    #epoch, satellite, elapsedEclipseTime, Voltage
    
    
    
       
    
    #if tvt.TlmyPrediction==Null
    

    
    