'''
Created on 1 feb. 2022

@author: pabli
'''

import os, sys, glob 
import pathlib

import time
from datetime import datetime, timedelta
import pytz
import pandas as pd
import numpy as np
import ephem


def findLastNoEclipse(sat_ephem, dt):
  
  ldt = dt-timedelta(seconds=1)
  sat_ephem.compute(ldt)
  while(not sat_ephem.eclipsed):
    ldt = ldt-timedelta(seconds=1)
    sat_ephem.compute(ldt)
    
  return ldt+timedelta(seconds=1)

if __name__ == '__main__':
  
  file = open('sacd_tle_20150527.txt', 'r')
  ol = file.read()
  lns = ol.split("\n")
  file.close()
  df = pd.read_csv("./LowOrbitSatellite.csv")#, index_col='datetime'
  #ls = 2015-05-27 08:51:06+00:00
  #.replace(tzinfo=pytz.UTC)
  #epoch = datetime.strptime("".join(ls), "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC) + timedelta(days=1)
  #epoch = datetime(2015,5,27, 8,51,6,0, tzinfo=pytz.UTC)
  #epoch = df[]
  sat_ephem = ephem.readtle('37673', lns[0], lns[1])
  df['dt'] = pd.to_datetime(df['datetime'])
  
  firstLight    = findLastNoEclipse(sat_ephem, df.iloc[0]['dt'])
  startEclipse  = 0
  cInEclipse = []
  elapsedTime = []
  
  eclipsed = False
  for value in df["dt"]:
    sat_ephem.compute(value)
    cInEclipse.append(sat_ephem.eclipsed)
    
    if not sat_ephem.eclipsed :
      if eclipsed:
        firstLight = value
      eclipsed = False
      elapsedTime.append((value-firstLight).seconds)
    else:
      if not eclipsed:
        #Antes estaba eclipsado y ahora no...
        startEclipse = value
      eclipsed = True
      elapsedTime.append(-(value-startEclipse).seconds)
      
    
    
  df['cInEclipse'] = cInEclipse
  df['elapsedTime'] = elapsedTime
  
  df.to_csv("./LowOrbitSatelliteWithEclipses.csv")
  #sat_ephem.compute(df.iloc[0]['dt'])
  #print("In eclipse: ", )
  ##df['calcInEclipse'] = cInEclipse(sat_ephem, df['dt']) 
  
  print(df.head())   
  
  """      
  
  df['inEclipse'] = 0;
    
  """