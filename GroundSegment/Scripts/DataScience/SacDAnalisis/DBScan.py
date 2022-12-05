'''
Created on 24-jul-2021

@author: pabli
'''
import os, sys, glob  
import pathlib

import time
from struct import unpack
from datetime import datetime, timedelta
from Scripts.DSUtils import getProjectPath
import pytz
from Scripts.DataScience.SacDAnalisis.UtilsSacd import plot_ellipse, loadFromDB, plot_gmm

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
from sklearn.cluster import DBSCAN
from kneed import KneeLocator
import numpy as np
from pandas.core.frame import DataFrame
from matplotlib import colors as mcolors

import random




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


##https://towardsdatascience.com/explaining-dbscan-clustering-18eaf5c83b31
"""
Terminar esto
def bestEpsilon():
  pca_eps_values = np.arange(0.2,1.5,0.1) 
  pca_min_samples = np.arange(2,5) 
  #Producto cartesiano
  pca_dbscan_params = list(product(pca_eps_values, pca_min_samples))
    
  pca_no_of_clusters = []
  pca_sil_score = []
  pca_epsvalues = []
  pca_min_samp = []
  for p in pca_dbscan_params:
      pca_dbscan_cluster = DBSCAN(eps=p[0], min_samples=p[1]).fit(pca_df)
      pca_epsvalues.append(p[0])
      pca_min_samp.append(p[1])
      pca_no_of_clusters.append(len(np.unique(pca_dbscan_cluster.labels_)))
      pca_sil_score.append(silhouette_score(pca_df, pca_dbscan_cluster.labels_))
  
  pca_eps_min = list(zip(pca_no_of_clusters, pca_sil_score, pca_epsvalues, pca_min_samp))
  pca_eps_min_df = pd.DataFrame(pca_eps_min, columns=['no_of_clusters', 'silhouette_score', 'epsilon_values', 'minimum_points'])
  pca_ep_min_df
"""

def getMarker(m):
  if m==-1:
    return 'x'
  else:
    return 'o'

def show_cluster(X, clusters):
  
  colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
 
  #by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
  #              for name, color in colors.items())
  
  by_hsv = [name for name, color in colors.items()]
  color_names = [name for name in by_hsv if len(name)>1]
  color_names.remove('red')
  random.shuffle(color_names)
  color_names.insert(0, 'red')
  
  df = DataFrame(dict(x=X[:,0],y=X[:,1], label=clusters))
  #colors = {-1:'red', 0:'blue', 1:'orange', 2:'green', 3:'skyblue', 4:'greenyellow', 5:'black', 6:'lime', 7:'indigo',
  #          8:}
  fig, ax = plt.subplots(figsize=(8,8))
  grouped = df.groupby('label')
  for key, group in grouped:
    group.plot(ax=ax, kind='scatter', x='x', y='y', label='Cluster '+str(key), color=color_names[key+1], marker=getMarker(key) )
  
  plt.xlabel('Normalized Panel 24 current')
  plt.ylabel('Normalized vBatteryVoltage')
  
  

  plt.show()
    
                 
  

if __name__ == '__main__':
  
  #df.plot(x=df.index, y='vBatAverage', style='o')
  try:
    #df = pd.read_csv("./LowOrbitSatellite.csv", index_col='datetime')
    df = pd.read_csv("./LowOrbitSatelliteWithEclipses.csv", index_col='datetime')
  except:
    df = loadFromDB()
  
  # ['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle', ISenseRS1','ISenseRS2',]
  #features = ['vBatAverage', 'BatteryDischarging']
  
  #TODO: Aplicar principal components a todo
  
  ccantPanels     = 24
  #TODO: Hacer DBScan
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
             'cInEclipse',  
             'elapsedTime',
             ]
  for i in range(ccantPanels):
    columns.append("V_MODULE_"+str(i+1)+"_SA")
  

  #Aca se comenta estas linea para cambiar la cantidad de features en el test
  
  #Solo 2
  #features = ['V_MODULE_24_SA', 'vBatAverage']
  #Solo datos del satelite(28)
  #features  = [column for column in columns if not column in ['cInEclipse','elapsedTime']]  
  #Todos los datos
  features     = columns
  
  
  
  #features = columns
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
  
  withAnomaly = False;
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
  
  dff = train
  min_samples = dff.shape[1]*2
  
  neighbors = NearestNeighbors(n_neighbors=20)
  neighbors_fit = neighbors.fit(dff)
  distances, indices = neighbors_fit.kneighbors(dff)
  distances = np.sort(distances, axis=0)
  distances = distances[:,1]
  


  # calculate and show knee/elbow
  kl = KneeLocator(
    x=np.arange(0,len(distances)), 
    y=distances,
    curve="convex", 
    direction="increasing")
  
  elbow_point = kl.elbow #elbow_point = kneedle.elbow
  print('min_samples:', min_samples, 'Elbow: ', elbow_point, distances[elbow_point]) #print('Elbow: ', elbow_point)
  #kl.plot_knee()
  
  eps  = distances[elbow_point]
  mdbscan = DBSCAN(eps=eps, min_samples=min_samples)
  clusters = mdbscan.fit_predict(dff)
  print("Cluster creados", str(list(set(clusters))), 
        "Cantidad sin clusters: ", sum(map(lambda x : x == -1, clusters)))
  
  mdbscan.fit_predict(, y)
  
  if(drawPlot):
    show_cluster(dff, clusters)
  
  
  
  