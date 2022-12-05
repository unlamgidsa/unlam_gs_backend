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
from Scripts.DataScience.SacDAnalisis.UtilsSacd import is_set, loadFromDB

from Telemetry.models.TlmyRawData import TlmyRawData
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.FrameType import FrameType

from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyRawData import TlmyRawData
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

if __name__ == '__main__':
  
  try:
    df = pd.read_csv("./SACD.csv", index_col='datetime')
  except:
    df = loadFromDB()
  
  
  
  #features = ['vBatAverage', 'BatteryDischarging']
  features = ['V_MODULE_1_SA', 'vBatAverage']
  
  df.index = pd.to_datetime(df.index)
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  X = df[features]
  #z = StandardScaler()
  #X = z.fit_transform(X)
  #x = X
  x = X.values
  nbrs = NearestNeighbors(n_neighbors=3
                          , algorithm='ball_tree')
  nbrs.fit(x)
  distances, indices = nbrs.kneighbors(x)
  
  
  #plt.plot(distances.mean(axis=1))
  #plt.show()
  
  abn_index = np.where(distances.mean(axis=1)>.5)
  plt.scatter(x[:,0], x[:,1])
  plt.scatter(x[abn_index,0], x[abn_index,1])
  plt.show()
  
  
  
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  """
  
  distances, indices = nbrs.kneighbors(x)
  df['health'] = distances.mean(axis=1)
  plt.plot(df['health'])
  plt.show()
  """
  
  """
  #df['mdate'] = pd.to_datetime(df['datetime'])
  df.drop('datetime', inplace=True, axis=1)
  df.drop('Unnamed: 0', inplace=True, axis=1)
  #df['anomaly'] = 0
  #'anomaly', 
  features = ['IInEclipse', 'BatteryDischarging']
  for i in range(23):
    features.append("V_MODULE_"+str(i+1)+"_SA")
  
  X = df[features]
  #df = df.sample(frac=0.1)
  train, test = train_test_split(X, shuffle=False, test_size=0.5)
   
  afrom = datetime(2015, 5, 27, 10, 0, 58, tzinfo=pytz.UTC) 
  ato   = datetime(2015, 5, 27, 10, 15, 18, tzinfo=pytz.UTC) 
  
  z = StandardScaler()
  train[features] = z.fit_transform(train)
  EM = GaussianMixture(n_components = 2)
  EM.fit(train)
  cluster = EM.predict(train)
  print("Score: ", silhouette_score(train, cluster))
  train['cluster'] = cluster
  
  #train.loc[(train['mdate']>afrom) & (train['mdate']<ato),'anomaly' ]        = 1
  #train.loc[(train['mdate']>afrom) & (train['mdate']<ato), 'V_MODULE_1_SA']  = 128
  #df['anomaly'].loc[( (df['mdate'] > afrom) & (df['mdate'] < ato))] = 1
  
   
  #bks = df.sample(frac=0.5,random_state=200)
  
  
  
  
  """
  
  """
  #z = StandardScaler()
  #X[features] = z.fit_transform(X)
  EM = GaussianMixture(n_components = 2)
  EM.fit(X)
  
  cluster = EM.predict(X)
  print("Score: ", silhouette_score(X, cluster))
  X['cluster'] = cluster
  
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  
  

  ax.scatter(np.array(X[features[0]]),
             np.array(X[features[1]]),
             np.array(X[features[2]]), marker="o", c=X["cluster"], s=40, cmap='Dark2')
  labels = ['x', 'y', 'z']
  
  for l, f in zip(labels, features):
    getattr(ax, "set_"+l+"label")(f)
    
  plt.show()
  
  print("Fin de programa")
  
  
  
  #X = df[['vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']] 
  #print(X)
  #corrMatrix = X.corr()
  #sn.heatmap(corrMatrix, annot=True)
  #plt.show()
  
  # multiple line plots
  #plt.plot( 'datetime', 'vBatAverage', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
  """

  
  #ANLG_p5V_FOUA   = 1604+671
  #ANLG_p5V_FOUB   = 1604+671
  """
  ff = []
  
  for r in raws:
    binary = r.getBlob()
    
    print(ff[len(ff)-1])
    
    ff.append(
      (struct.unpack(">H", binary[bvBatAverage:bvBatAverage+struct.calcsize("H")])[0]*0.01873128+-38.682956,#vBatAverage
      struct.unpack("B", binary[bV_MODULE_01_SA:bV_MODULE_01_SA+struct.calcsize("B")])[0]*0.001766351+-3.6390652,#V_MODULE_01_SA
      struct.unpack("B", binary[bSP_MMB2_1:bSP_MMB2_1+struct.calcsize("B")])[0]*0.000574857-1.1883427,#SP_MMB2_1
      is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],5),#batState
      struct.unpack("B", binary[bISenseRS1:bISenseRS1+struct.calcsize("B")])[0]*0.03921567+-80.95683,#ISenseRS1
      struct.unpack("B", binary[bISenseRS2:bISenseRS2+struct.calcsize("B")])[0]*0.03921567+-80.95683,
      struct.unpack("B", binary[bIdMinor:bIdMinor+struct.calcsize("B")])[0],
      struct.unpack("B", binary[bTEMP_1A_HSC:bTEMP_1A_HSC+struct.calcsize("B")])[0]*0.176936624*1773.76349,
      #struct.unpack("B", binary[bstatusPCS2:bstatusPCS2+struct.calcsize("B")])[0],
      BitArray(binary[bstatusPCS2]).bin,
      struct.unpack("B", binary[bTEMP_1A_HSC:bTEMP_1A_HSC+struct.calcsize("B")])[0]*0.003266528-6.7564767,
      
      ),#0x70, 0x71, 0x72, 0x73, 0x74 
      )
    
    print(ff[len(ff)-1])
  """  
  #df = pd.DataFrame(data, columns =['Name', 'Age', 'Score'])
  #print(BitArray(binary[bBatState]).bin)
  #print(batState[len(batState)-1])
  #print(ISenseRS1[len(ISenseRS1)-1],ISenseRS2[len(ISenseRS2)-1])
    
    
    
    
  #df = pd.DataFrame(list(zip(lst, lst2)), columns =['Name', 'val'])
    