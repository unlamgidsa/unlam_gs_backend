'''
Created on 3 abr. 2020

@author: pablo
'''

from GroundSegment.celery import loadDjangoApp


#import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy import stats
import matplotlib.pyplot as plt



loadDjangoApp();

from django_pandas.managers import DataFrameManager
from django_pandas.io import read_frame
import pandas as pd
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType
from django.db import connection

if __name__ == '__main__':
    #Analisis de capacitacion, relacion entre la maxima y minima temperatura en un dia cualquiera
    
    temps_tita_sql = """Select tv1."calFValue" as cpu_cell_temp, tv2."calFValue" as mirror_cell_C
                        from "Telemetry_tlmyvar" as tv1 inner join "Telemetry_tlmyvar" as tv2
                        on tv1.tstamp=tv2.tstamp
                        where tv1.code='CPU_C' and tv2.code='mirror_cell_C'
                        order by tv1.tstamp
                        limit 100"""
    
    
    
    df = pd.read_sql_query(sql=temps_tita_sql, con=connection)
    
    df.plot.scatter (x="cpu_cell_temp", y="mirror_cell_c")
    plt.show()
    """

    cpu_temps           = TlmyVar.objects.filter(code="CPU_C").order_by('tstamp').values('calIValue', 'tstamp')
    mirror_cell_temp    = TlmyVar.objects.filter(code="mirror_cell_C").order_by('tstamp').values('calIValue', 'tstamp')
    
    df = read_frame(cpu_temps)
    dft = read_frame(mirror_cell_temp)
    
    lower_bound = 1
    upper_bound = 1
    ra = range(0,6215)
    #plt.plot(df['tstamp'], df['calIValue'])
    X = df['calIValue']
    X = X[X.between(X.quantile(.05), X.quantile(.995))]
    
    # without outliers
    
    plt.hist(df['calIValue'])
    plt.show()
    """
    print("Fin de algoritmo")
    
    
    
    