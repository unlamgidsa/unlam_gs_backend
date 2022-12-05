'''
Created on 17 feb. 2022

@author: pabli
'''
'''
Created on 24-jul-2021

@author: pabli
'''
import os, sys, glob 
import time
from struct import unpack
from datetime import datetime, timedelta
from Scripts.DSUtils import getProjectPath
import pytz
from Scripts.DataScience.SacDAnalisis.UtilsSacd import plot_ellipse, is_set, loadFromDB, plot_gmm, draw_ellipse
import struct
import pandas as pd
from bitstring import BitArray, BitStream
import seaborn as sn
import matplotlib.pyplot as plt
#import tensorflow as tf
#from tensorflow.keras.models import Model

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np


"""
In the case where multiple univariate time series from the same domain are used, the extent of their
relationship can be expressed using correlation. It is assumed that anomalous behaviour can be derived from
the discrepancy in their correlation
"""

def n_components_plot(X):
  n_components = np.arange(1, 21)
  models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X)
            for n in n_components]

  plt.plot(n_components, [m.bic(X) for m in models], label='BIC')
  plt.plot(n_components, [m.aic(X) for m in models], label='AIC')
  plt.legend(loc='best')
  plt.xlabel('n_components');
  plt.show()
  
def getBestGMM(X):
    lowest_bic = np.infty
    bic = []
    n_components = np.arange(1, 20)
    covariance_types = ['full', 'tied', 'diag', 'spherical']
    for cv_type in covariance_types:
        for n_c in n_components:
            # Fit a Gaussian mixture with EM
            gmm = GaussianMixture(n_components=n_c,
                                          covariance_type=cv_type, random_state=0)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm

    return best_gmm


def n_components(X):
  n_components = np.arange(1, 20)
  models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X) for n in n_components]
  
  min_val = models[0].bic(X)
  result = models[0].n_components
  for m in models[1:]:
    bx = m.bic(X)
    if bx<min_val:
      result  = m.n_components  
      min_val = bx
      
      
  return result
 
  #plt.plot(n_components,, label='BIC')
  #plt.plot(n_components, [m.aic(X) for m in models], label='AIC')
  #plt.legend(loc='best')
  #plt.xlabel('n_components');
  #plt.show()
#aca analiza con test
  #https://www.kaggle.com/albertmistu/detect-anomalies-using-gmm
  #https://www.cienciadedatos.net/documentos/py23-deteccion-anomalias-gmm-python.html
  
#https://jakevdp.github.io/PythonDataScienceHandbook/05.12-gaussian-mixtures.html
if __name__ == '__main__':
  
  #df.plot(x=df.index, y='vBatAverage', style='o')
  
  df = pd.read_csv("./LowOrbitSatellite.csv", index_col='datetime')
  
  # ['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle', ISenseRS1','ISenseRS2',]
  #features = ['vBatAverage', 'BatteryDischarging']
  
  
  
  ccantPanels     = 24
  
  columns = ['vBatAverage', 
             'IInEclipse', 
             'BatteryEmergency',
             'BatterySaveMode',
             'BatteryOvertemp',
             'BatteryOvervoltage',
             'BatteryUndervoltage',
             'BatteryDischarging',
             'BatteryOvertemperature', 
             'bvrCycle',
             'ISenseRS1',
             'ISenseRS2',
             ]
  for i in range(ccantPanels):
    columns.append("V_MODULE_"+str(i+1)+"_SA")
  
  #features = ['V_MODULE_24_SA', 'vBatAverage']
  features = columns
  drawPlot = len(features)==2
  anormal_feature = 'V_MODULE_24_SA'
  testpercent = 0.2
  
  df.index = pd.to_datetime(df.index)
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  #iLoc=>rows and columns
  
  
  limitData = True
  
  if(limitData):
    afrom = df.index[0]
    ato   = afrom+timedelta(days=2)
    df    = df.loc[(df.index>afrom) & (df.index<ato)] 
    #df = df.iloc[0:12000]
  
  withAnomaly = True;
  if withAnomaly:
    tt = round(len(df)*(testpercent/4))
    #df[-tt].datetime
    #df.loc[df.datetime > df[-tt].datetime, anormal_feature] = 128
    
    for i in range(1,tt):
      df.iloc[-i, df.columns.get_loc(anormal_feature)] = 129
    val = 128
    while(val<220):
      df.iloc[-i, df.columns.get_loc(anormal_feature)] = val
      val=val+1
      i=i+1
  
  #df.to_csv("./SACD.csv")
  print("fechas de inicio y fin de bloque: ", df.iloc[[0, -1],[0]])
  
  dff = df[features]
  z = StandardScaler()
  dff = z.fit_transform(dff)
  train, test = train_test_split(dff, shuffle=False, test_size=testpercent)
  #x = X
  #X = X.values
  #n_components_plot(X)
  #n_com = n_components(train)
  #n_com = 3
  #print("Componentes autoseleccionados: ", n_com)
  #gmm = GaussianMixture(n_components=n_com, covariance_type='full').fit(train)
  gmm = getBestGMM(train)
  labels = gmm.predict(train)
  probs = gmm.predict_proba(train)
  #Outlier Detection Algorithm Based on Gaussian Mixture Model
  #outliers = np.nonzero(p<epsilon)[0]
  print("Score: ", silhouette_score(train, labels))
  print("n_components: ", gmm.n_components)
  print("covariance_type: ", gmm.covariance_type)
  #https://www.datatechnotes.com/2020/04/anomaly-detection-with-gaussian-mixture.html
  scores = gmm.score_samples(train)
  #thresh = np.quantile(scores, .001)
  #index = np.where(scores <= thresh)
  #values = X[index]
  thresh =  scores.min()
  print("Minimun score:", thresh)
  
  #Dibujar sin errores
  if drawPlot:
    fig=plt.figure(figsize=(8,6))   
    dftrain = pd.DataFrame(data=train, columns=features)
    dftrain['cluster'] = labels
    mscores =  ['x' if v < thresh else 'v' for v in scores]
    mcolors =  ['r' if v < thresh else 'b' for v in scores]
    #fig=plt.figure(figsize=(10,10))   
    size = 50 * probs.max(1) ** 2 # square emphasizes differences
    for k,d in dftrain.groupby('cluster'):
        plt.scatter(d[features[0]], d[features[1]], label="Cluster "+str(k), cmap='viridis');
        #ax.scatter(d['attempts'], d['success'], label=k)
    
    plt.xlabel('Normalized Panel 24 current');
    plt.ylabel('Normalized vBatteryVoltage');
    plot_gmm(gmm, train, labels)
    plt.legend()
    plt.grid(True)
    
    plt.show()
  #plt.close()
  #plt.figure().clear()
  scores = gmm.score_samples(test)
  anomalies =  scores[scores<thresh]
  print("Total Anomalies: ", len(anomalies))
  if drawPlot:
    fig=plt.figure(figsize=(8,6)) 
    dftest = pd.DataFrame(data=test, columns=features)
    size = 50 * probs.max(1) ** 2 # square emphasizes differences
    #plt.scatter(train[:, 0], train[:, 1], c=labels, cmap='viridis', s=size);
    dftest['label'] = ['Test Anomaly' if v < thresh else 'Test Nominal' for v in scores]
    dftest['color'] = ['r' if v < thresh else 'b' for v in scores]
    dftest['mark'] =  ['x' if v < thresh else 'v' for v in scores]
    for k,d in dftest.groupby('label'):
        plt.scatter(d[features[0]], d[features[1]], label=k, c=d.iloc[0]['color'], marker=d.iloc[0]['mark'], cmap='viridis');
     
    
    #plt.scatter(test[:, 0], test[:, 1], marker='x', color=mcolors, cmap='viridis');
    plt.xlabel('Normalized Panel 24 current');
    plt.ylabel('Normalized vBatteryVoltage');
    plt.legend()
    #plt.scatter(values[:,0], values[:,1], marker='x', color='r')
    #plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
    plot_ellipse(gmm)
    plt.show()
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  print("stop")
  