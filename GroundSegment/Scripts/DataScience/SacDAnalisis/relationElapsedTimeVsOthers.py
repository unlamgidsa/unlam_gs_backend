'''
Created on 2 feb. 2022

@author: pabli
'''

import os, sys, glob 
import time
from datetime import datetime, timedelta
import pytz
from Scripts.DataScience.SacDAnalisis.UtilsSacd import plot_ellipse, loadFromDB, plot_gmm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

#import tensorflow as tf
#from tensorflow.keras.models import Model
import numpy as np

#https://unidata.github.io/python-training/workshop/Time_Series/basic-time-series-plotting/

if __name__ == '__main__':
  try:
    #df = pd.read_csv("./LowOrbitSatellite.csv", index_col='datetime')
    df = pd.read_csv("./LowOrbitSatelliteWithEclipses.csv", index_col='datetime')
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
               'dt',
               'cInEclipse',  
               'elapsedTime',
               ]
    for i in range(ccantPanels):
      columns.append("V_MODULE_"+str(i+1)+"_SA")
    #achico el dataset para la prueba
    
    df.index = pd.to_datetime(df.index)
    limitData = True
    if(limitData):
      afrom = df.index[0]
      ato   = afrom+timedelta(days=2)
      df    = df.loc[(df.index>afrom) & (df.index<ato)] 
    
    
    X = df[['vBatAverage', 'IInEclipse', 'BatteryDischarging', 'cInEclipse', 'elapsedTime']] 
    #print(X)
    corrMatrix = X.corr()
    sn.heatmap(corrMatrix, annot=True)
    plt.show()
    """
    
    #df = df.head(5000)
    
  
    
    features = ['V_MODULE_24_SA', 'elapsedTime', 'vBatAverage']
    tserie   = df['dt']
    df = df[features]
    
   
   
   
 
   
    
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df.to_numpy())
    df_scaled = pd.DataFrame(df_scaled, columns=['V_MODULE_24_SA', 'elapsedTime', 'vBatAverage'])
    
    df = df_scaled
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    
    
    # Specify how our lines should look
    ax.plot(tserie, df.elapsedTime, color='tab:orange', label='elapsedTime')
    ax.plot(tserie, df.V_MODULE_24_SA, color='tab:olive', label='V_MODULE_24_SA')
    ax.plot(tserie, df.vBatAverage, color='tab:green', label='vBatAverage')
    
    # Same as above
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Scaled values')
    ax.set_title('V_MODULE_24_SA/elapsedTime/vBatAverage')
    ax.grid(True)
    ax.legend(loc='upper left');
    plt.show()
    
    
    """

    
    print("Fin")
    
  except Exception as ex:
    print("No se puede cargar el dataset", ex)