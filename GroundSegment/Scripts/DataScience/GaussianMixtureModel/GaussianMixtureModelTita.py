'''
Created on 21-jul-2021

@author: pabli
'''
import warnings
from pyasn1_modules.rfc5084 import aes
warnings.filterwarnings('ignore')
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_score
import pandas as pd
from plotnine import *

"""%matplotlib inline"""
def deleteOutlier(df, field):
    Q1 = np.percentile(df[field], 25, interpolation = 'midpoint')  
    Q2 = np.percentile(df[field], 50, interpolation = 'midpoint')  
    Q3 = np.percentile(df[field], 75, interpolation = 'midpoint')  
    IQR = Q3 - Q1  
    #print('Interquartile range is', IQR) 
    low_lim = Q1 - 2 * IQR 
    up_lim = Q3 + 2 * IQR 
  
    #Si los limites son distintos darle gas
    if low_lim!=up_lim:
        #df = df[(df['closing_price'] >= 99) & (df['closing_price'] <= 101)]
        #df = df[df['closing_price'].between(99, 101)]
        df = df[df[field].between(low_lim, up_lim)]
    
    return df

if __name__ == '__main__':
  bk = pd.read_csv("./../tita.csv")
  
  #features = ['CPU_C', 'temp_imo_c', 'pcm_3v3_v']
  #features = ['nice_battery', 'elapsedTime', 'sunvectorZ']
   
  features = ['pcm_3v3_a', 'pcm_3v3_v', 'nice_battery'] 
  print(len(bk.index))
  for c in features:
    bk = deleteOutlier(bk, c)
  print(len(bk.index))
  bks = bk.sample(frac=0.1,random_state=200)
  print(len(bks.index))
  X = bks[features]
  
  #z = StandardScaler()
  #X[features] = z.fit_transform(X)
  EM = GaussianMixture(n_components = 4)
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