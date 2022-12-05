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
from Scripts.DataScience.SacDAnalisis.UtilsSacd import is_set, loadFromDB, plot_gmm, draw_ellipse
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
                                          covariance_type=cv_type)
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
  try:
    df = pd.read_csv("./SACD.csv", index_col='datetime')
  except:
    df = loadFromDB()
  
  # ['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle', ISenseRS1','ISenseRS2',]
  #features = ['vBatAverage', 'BatteryDischarging']
  #df['datetime'] = pd.to_datetime(df.index.values)
  #plt.plot(df['datetime'], df['vBatAverage'])
  #plt.scatter(df.index.values, df['vBatAverage'])
  #plt.show() # Depending on whether you use IPython or interactive mode, etc.
  
  plt.scatter(df['V_MODULE_24_SA'], df['vBatAverage'], cmap='viridis');
  plt.xlabel('Panel 24 current(Raw)');
  plt.ylabel('vBatteryVoltage');  
  plt.show()
  
  plt.scatter(df['V_MODULE_24_SA'], df['ISenseRS1'], cmap='viridis');
  plt.xlabel('Panel 24 current(Raw)');
  plt.ylabel('ISenseRS1(Raw)');  
  plt.show()
  
  plt.scatter(df['V_MODULE_24_SA'], df['ISenseRS1'], cmap='viridis');
  plt.xlabel('Panel 24 current(Raw)');
  plt.ylabel('ISenseRS2(Raw)');  
  plt.show()