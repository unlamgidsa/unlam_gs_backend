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
    low_lim = Q1 - 4 * IQR 
    up_lim = Q3 + 4 * IQR 
    #print('low_limit is', low_lim) 
    #print('up_limit is', up_lim) 
    #Si los limites son distintos darle gas
    if low_lim!=up_lim:
        #df = df[(df['closing_price'] >= 99) & (df['closing_price'] <= 101)]
        #df = df[df['closing_price'].between(99, 101)]
        df = df[df[field].between(low_lim, up_lim)]
    
    return df

if __name__ == '__main__':
  bk = pd.read_csv("./../tita.csv")
  
  print(bk.head())
  features = ['pcm_3v3_v', 'pcm_3v3_a', 'pcm_5v_a']
  print(len(bk.index))
  bks = bk.sample(frac=0.1,random_state=200)
  
  print(len(bks.index))
  
  X = bks[features]
  z = StandardScaler()
  
  X[features] = z.fit_transform(X)
  
  EM = GaussianMixture(n_components = 4)
  EM.fit(X)
  
  cluster = EM.predict(X)
  print("Score: ", silhouette_score(X, cluster))
  X['cluster'] = cluster
  
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  x = np.array(X['pcm_3v3_v'])
  y = np.array(X['pcm_3v3_a'])
  z = np.array(X['pcm_5v_a'])
  ax.scatter(x,y,z, marker="o", c=X["cluster"], s=40, cmap='Dark2')
    
  ax.set_xlabel('pcm_3v3_v')
  ax.set_ylabel('pcm_3v3_a')
  ax.set_zlabel('pcm_5v_a')
  plt.show()
  
  print("Fin de programa")