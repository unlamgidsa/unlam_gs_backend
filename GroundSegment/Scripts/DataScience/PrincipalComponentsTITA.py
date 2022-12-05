# -*- coding: utf-8 -*-
'''
Created on 04-mar-2021

@author: pabli
'''

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


import os; 
from Scripts.DSUtils import getProjectPath, generateDSQuery
from datetime import datetime
from sklearn.model_selection._split import train_test_split
from sklearn.linear_model._logistic import LogisticRegression
from numpy.random.mtrand import logistic

BASE_DIR = getProjectPath()
os.chdir(BASE_DIR)

import sys; 
print('%s %s' % (sys.executable or sys.platform, sys.version))
os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import numpy as np
import pandas as pd
from django.db import connection
import matplotlib.pyplot as plt

if __name__ == '__main__':
  
  target = 'CPU_C'
  varnames = [
            'battery_amps', 
            'CPU_C', 
            'gyro_x', 
            'gyro_y', 
            'gyro_z', 
            'magnetometer_x', 
            'magnetometer_y', 
            'magnetometer_z', 
            'mirror_cell_C', 
            'nice_battery', 
            'pcm_3v3_a', 
            'pcm_3v3_v', 
            'pcm_5v_a', 
            'pcm_5v_v', 
            'sunvectorX', 
            'sunvectorY', 
            'sunvectorZ', 
            'temp_imo_c', 
            ]

  features = [x for x in varnames if x != target]
  
  afrom = datetime(2020, 10, 5, 0, 0, 0) 
  ato   = datetime(2020, 11, 1, 0, 0, 0)
  
  query = generateDSQuery(vars=varnames, afrom=afrom, ato=ato)
  df = pd.read_sql_query(sql=query, con=connection)
  """
  
  x = df.loc[:,features].values
  y = df.loc[:,[target]].values
  
  trainds, testds, trainlbl = train_test_split(x,y,test_size=1/7.0,random_state=0)
  
  scaler = StandardScaler()
  trainds = scaler.fit(trainds)
  testds = scaler.fit(testds)
  
  pca = PCA(0.8) #n_components=2
  
  trainds = pca.transform(trainds)
  testds = pca.transform(testds)
  logisticRegr = LogisticRegression(solver='lbfgs')
  logisticRegr.fit(trainds, trainlbl)
  
  logisticRegr.predict(testds[0].reshape(-1,1))
  
   
  
  
  
  
  
  x = StandardScaler().fit_transform(x)
  principalComponents = pca.fit_transform(x)
  principalDf = pd.DataFrame(data=principalComponents, columns=['pc1', 'pc2'])
  
  finalDf = pd.concat([principalDf, df[[target]]], axis=1)
  
  fig = plt.figure(figsize=(8,8))
  ax =fig.add_subplot(1,1,1)
  ax.set_xlabel('pc1', fontsize=15)
  ax.set_xlabel('pc2', fontsize=15)
  ax.set_title('2c', fontsize=20)
  
  
  
   
  
  #normalizamos los datos
  scaler=StandardScaler()
  df = dataframe.drop(['CPU_C'], axis=1) # quito la variable dependiente "Y"
  df = dataframe.drop(['tstamp'], axis=1)
  scaler.fit(df) # calculo la media para poder hacer la transformacion
  X_scaled=scaler.transform(df)# Ahora si, escalo los datos y los normalizo
  
  #Instanciamos objeto PCA y aplicamos
  pca=PCA(n_components=2) # Otra opci�n es instanciar pca s�lo con dimensiones nuevas hasta obtener un m�nimo "explicado" ej.: pca=PCA(.85)
  pca.fit(X_scaled) # obtener los componentes principales
  X_pca=pca.transform(X_scaled) # convertimos nuestros datos con las nuevas dimensiones de PCA
  
  print("shape of X_pca", X_pca.shape)
  expl = pca.explained_variance_ratio_
  print(expl)
  print('suma:',sum(expl[0:8]))
  
  
  #graficamos el acumulado de varianza explicada en las nuevas dimensiones
  plt.plot(np.cumsum(pca.explained_variance_ratio_))
  plt.xlabel('number of components')
  plt.ylabel('cumulative explained variance')
  plt.show()
  """
  
  
  print("fin")
  