'''
Created on 04-mar-2021

@author: pabli
'''
from random import random

import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sn
import ppscore as pps

import os; 
from Scripts.DataScience.DSUtils import getProjectPath, generateDSQuery,\
  deleteOutlier
from datetime import datetime
from Scripts.DataScience.Models import PolinomialRegresionModel
from statsmodels.genmod.tests.results.res_R_var_weight import dir_path



BASE_DIR = getProjectPath()
os.chdir(BASE_DIR)

import sys; 
print('%s %s' % (sys.executable or sys.platform, sys.version))



def corr_heatmap(df):
    ax = sn.heatmap(df.corr(), vmin=-1, vmax=1, cmap="BrBG", linewidths=0.5, annot=True)
    #sns.heatmap(df.corr(), annot=True)
    ax.set_title('Correlation matrix')
    return ax



target = 'CPU_C'
varnames = ["CPU_C", 
            "mirror_cell_C", 
            "temp_imo_c", 
            "nice_battery", 
            "pcm_3v3_v",
            "pcm_3v3_a",
            "pcm_5v_v",
            "pcm_5v_a",
            "sunvectorX",
            "sunvectorY",
            "sunvectorZ"
            ]

features = [x for x in varnames if x != target]


dir_path = os.path.dirname(os.path.realpath(__file__))
try:  
  df = pd.read_csv(dir_path+"\\tita.csv")
except Exception as ex:
  os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 
  sys.path.append(BASE_DIR)
  os.chdir(BASE_DIR)
  import django
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()
  from django.db import connection
  from GroundSegment.models.Satellite import Satellite
  sat = Satellite.objects.get(code="TITA")
  
  afrom = datetime(2020, 1, 1, 0, 0, 0) 
  ato   = datetime(2021, 3, 16, 0, 0, 0)
  query = generateDSQuery(vars=varnames, afrom=afrom, ato=ato, filter_outlier=False)
  df = pd.read_sql_query(sql=query, con=connection)
  df['month'] = df['tstamp'].dt.month
  df['inEclipse'] = df.apply(lambda x: 1 if sat.inEclipse(x['tstamp']) else 0, axis=1)
  df['elapsedTime'] = df.apply(lambda x: sat.eclipseElapsedTime(x['tstamp']), axis=1)
    
  df.to_csv(dir_path+"\\tita.csv");

"""
msk = np.random.rand(len(df)) < 0.8
df_train = df[msk]
df_test = df[~msk]
"""
#print(pps.score(df, "CPU_C", "mirror_cell_C"))
#corr_heatmap(df)
#sn.heatmap(df.corr(), annot=True)
#print(pps.score(df, "CPU_C", "temp_imo_c"))
#print(pps.score(df, "CPU_C", "mirror_cell_C"))
#sn.heatmap(df.corr(), annot=True)
df['tstamp'] = pd.to_datetime(df['tstamp'])
df = df[df['tstamp'].astype('datetime64[ns]')>datetime(2020, 1, 1, 0, 0, 0)]
df = df[df['tstamp'].astype('datetime64[ns]')<datetime(2021, 3, 16, 0, 0, 0)]

#extraigo columnas que no esten activadas

varnames = ["CPU_C", 
            #"mirror_cell_C", 
            "temp_imo_c", 
            "nice_battery", 
            "pcm_3v3_v",
            "pcm_3v3_a",
            "pcm_5v_v",
            "pcm_5v_a",
            "sunvectorX",
            "sunvectorY",
            "sunvectorZ",
            'inEclipse',
            'elapsedTime',
            
            ]

columns = list(df)
for c in columns:
  if not c in varnames:
    df = df.drop([c,], axis=1)
    

print("Rows before outlier filter ", len(df.index));
for c in varnames:
  df = deleteOutlier(df, c)
print("Rows after outlier filter ", len(df.index));

#afrom = datetime(2020, 1, 1, 0, 0, 0) 
#ato   = datetime(2021, 3, 16, 0, 0, 0)
  

"""
matrix_pps = pps.matrix(df).pivot(columns='x', index='y',  values='ppscore')  
sn.heatmap(matrix_pps, annot=True)
plt.show()


plt.scatter(df["CPU_C"], df["temp_imo_c"], alpha=0.5)
plt.show()
"""

xvars = ["temp_imo_c", "pcm_3v3_v", "pcm_3v3_a", "pcm_5v_v", "pcm_5v_a",];
yvar = ['CPU_C']
PolinomialRegresionModel(df, xvars, yvar)



print("fin")