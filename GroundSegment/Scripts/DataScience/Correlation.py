'''
Created on 01-mar-2021

@author: pabli
'''

from GroundSegment.celery import loadDjangoApp


#import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.utils.timezone import utc
from Scripts.DSUtils import generateDSQuery

loadDjangoApp();

from django_pandas.managers import DataFrameManager
from django_pandas.io import read_frame
import pandas as pd
from Telemetry.models.TlmyVar import TlmyVar
from Telemetry.models.TlmyVarType import TlmyVarType
from django.db import connection
from GroundSegment.models.Satellite import Satellite
from django.db.models import F
from django.db.models import Count

import seaborn as sn
import matplotlib.pyplot as plt

if __name__ == '__main__':
  """
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
              "sunvectorZ"]
  """
  
  varnames = [#'ant_dep_status', 
              #'aocs_mode', 
              'battery_amps', 
              'CPU_C', 
              #'current_mode', 
              #'current_state', 
              #'experiments_failed', 
              #'experiments_run', 
              #'fine_gyro_x', 
              #'fine_gyro_y', 
              #'fine_gyro_z', 
              #'free', 
              'gyro_x', 
              'gyro_y', 
              'gyro_z', 
              #'last_boot_reason', 
              #'last_experiment_run', 
              #'last_seq_num', 
              #'low_voltage_counter', 
              'magnetometer_x', 
              'magnetometer_y', 
              'magnetometer_z', 
              'mirror_cell_C', 
              'nice_battery', 
              #'pcm_3v3_a', 
              #'pcm_3v3_v', 
              #'pcm_5v_a', 
              #'pcm_5v_v', 
              #'raw_battery', 
              #'rtc_s', 
              'sunvectorX', 
              'sunvectorY', 
              'sunvectorZ', 
              'temp_imo_c', 
              #'uptime_s', 
              #'wheel_1', 
              #'wheel_2', 
              #'wheel_3', 
              #'wheel_4'
              ]
  
  
  #varnames = list(Satellite.objects.get(code="TITA").tmlyVarType.all().values_list("code", flat=True))
  
  afrom = datetime(2020, 2, 1, 0, 0, 0) 
  ato   = datetime(2021, 3, 16, 0, 0, 0)
  
  query = generateDSQuery(vars=varnames, afrom=afrom, ato=ato)
  
  
  df = pd.read_sql_query(sql=query, con=connection)
  #corrMatrix = df.corr()
  #print (corrMatrix)
  
  #sn.heatmap(corrMatrix, annot=True)
  #fig = plt.show()
  #plt.close(fig)
  
  df['tstamp']
  df['magnetometer_x']
  
  df = df[df['CPU_C']<50]
  df = df[df['CPU_C']>-50]
  
  df = df[df['temp_imo_c']<50]
  df = df[df['temp_imo_c']>-50]
  
  
  plt.plot(df['tstamp'], df['CPU_C'], 'r') # plotting t, a separately 
  plt.plot(df['tstamp'], df['temp_imo_c'], 'b') # plotting t, b separately 
  #plt.plot(t, c, 'g') # plotting t, c separately 
  plt.show()
  
  #CPU_C parece estar correlacionada con magnetometer_x y temp_imo_c
  
  
  #df.plot.scatter (x="CPU_C", y="mirror_cell_c")
  #plt.show()
      
  

  
  
  
  """
  sat = Satellite.objects.get(code="TITA")
  
  varnames = ["CPU_C", "mirror_cell_C", "temp_imo_c"]
  
  
  start_date = datetime.now(utc);
  end_date =   start_date - timedelta(days=365)
  
  #Reservation.objects.values('day').annotate(cnt=models.Count('id')).filter(cnt__lte=5)
  
  
  
  
  #Estan todas las variables listadas para cada instante
  nres = TlmyVar.objects.filter(tstamp__range=(end_date, start_date), outlier=False,code__in=varnames)\
                 .values('tstamp')\
                 .annotate(total=Count('tstamp'))\
                 .filter(total=len(varnames))
                 
  
  data = {}
  
  
  for el in nres:
    vars =  TlmyVar.objects.filter(code__in=varnames, tstamp=el['tstamp']).order_by('code')
    data[el['tstamp']] = list(vars.values_list('calFValue', flat=True))
  
  df = pd.DataFrame(data,columns=varnames)
    
  corrMatrix = df.corr()
  #print (corrMatrix)
    
    
  sn.heatmap(corrMatrix, annot=True)
  plt.show()
    
  TlmyVar.objects.filter(outlier=False, code__in=varnames).values('tstamp').annotate(total=Count('tstamp')).filter(total=len(varnames))
  
  res = TlmyVar.objects.filter(tstamp__range=(end_date, start_date), 
                               outlier=False, 
                               code__in=varnames)\
                               .annotate(varcount=Count('tstamp'))\
                               .filter(varcount=len(varnames))
  
  res = TlmyVar.objects.filter(tstamp__range=(end_date, start_date), 
                               outlier=False, 
                               code__in=varnames)\
                               .values_list('tstamp', flat=True)\
                               .distinct()\
                               .order_by('tstamp')
    
  """  
                        
  #vars = TlmyVar.objects.filter(tstamp__in=res, code__in=varnames).order_by('tstamp', 'code')
  
  
    
    
  """
  for r in res:
    vars = TlmyVar.objects.filter(tstamp=r, code__in=varnames)
    if vars.count()>2:
      print(vars.count())
  """
  
    
  
  
  
  
  """
  temps_tita_sql = "Select tv1."calFValue" as cpu_cell_temp, tv2."calFValue" as mirror_cell_C, tv3."calFValue" as temp_imo_c
                      from "Telemetry_tlmyvar" as tv1 inner join "Telemetry_tlmyvar" as tv2
                      on tv1.tstamp=tv2.tstamp inner join "Telemetry_tlmyvar" tv3 on tv2.tstamp=tv3.tstamp
                      where tv1.code='CPU_C' and tv2.code='mirror_cell_C' and tv3.code='temp_imo_c' and
                      tv1.outlier=false and tv2.outlier=false and tv2.outlier=false
                      order by tv1.tstamp
                      limit 1000"
  
  
  df = pd.read_sql_query(sql=temps_tita_sql, con=connection)
  
  df.plot.scatter (x="cpu_cell_temp", y="mirror_cell_c")
  plt.show()
      
  print(sat.code)
  """
  print("Fin de programa")
    
    
    