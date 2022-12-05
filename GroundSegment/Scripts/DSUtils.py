'''
Created on 01-mar-2021

@author: pabli
'''

"""
Select tv1.tstamp, tv1."calFValue" as cpu_cell_temp, tv2."calFValue" as mirror_cell_C, tv3."calFValue" as temp_imo_c
                        from "Telemetry_tlmyvar" as tv1 inner join "Telemetry_tlmyvar" as tv2
                        on tv1.tstamp=tv2.tstamp inner join "Telemetry_tlmyvar" tv3 on tv2.tstamp=tv3.tstamp
                        where tv1.code='CPU_C' and tv2.code='mirror_cell_C' and tv3.code='temp_imo_c' and
            tv1.outlier=false and tv2.outlier=false and tv2.outlier=false
                        order by tv1.tstamp
                        limit 1000
                        """

import socket
import numpy as np

def doubleQuoted(value):
  return "\""+value+"\""


def simpleQuoted(value):
  return "\'"+value+"\'"


def getProjectPath():
  
  hostname=socket.gethostname()
  if hostname=='NB-PABLO':
    return "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
  else:
    return ""
    
    
    
def deleteOutlier(df, field):
  Q1 = np.percentile(df[field], 25, interpolation = 'midpoint')  
  Q2 = np.percentile(df[field], 50, interpolation = 'midpoint')  
  Q3 = np.percentile(df[field], 75, interpolation = 'midpoint')  
  IQR = Q3 - Q1  
  print('Interquartile range is', IQR) 
  low_lim = Q1 - 1.5 * IQR 
  up_lim = Q3 + 1.5 * IQR 
  print('low_limit is', low_lim) 
  print('up_limit is', up_lim) 
  #Si los limites son distintos darle gas
  if low_lim!=up_lim:
    #df = df[(df['closing_price'] >= 99) & (df['closing_price'] <= 101)]
    #df = df[df['closing_price'].between(99, 101)]
    df = df[df[field].between(low_lim, up_lim)]
    
  return df
    

def generateDSQuery(**kwargs):
  #vars, afrom, ato, limit
  vars = kwargs["vars"]
  filter_outlier = 0#kwargs["filter_outlier"] 
    
  i = 1
  table = "Telemetry_tlmyvar"
  
  alias = []
  for t in vars:
    alias.append("tv"+str(i))
    i = i + 1;
    
  aselect = "select "+alias[0]+"."+doubleQuoted("tstamp") 
  for v, a in zip(vars, alias):
    aselect += ", CAST("+a+"."+doubleQuoted("calSValue")+"as float) as "+doubleQuoted(v)
    
    
 
  afrom = "\nfrom "+doubleQuoted("Telemetry_tlmyvar")+" as "+alias[0]+"\n"
  for i in range(1, len(alias)):
    afrom += " inner join "+doubleQuoted("Telemetry_tlmyvar")+" as "+alias[i]+" on "+alias[i-1]+".tstamp="+alias[i]+".tstamp"+"\n"
  
  """
  where tv1.code='CPU_C' and tv2.code='mirror_cell_C' and tv3.code='temp_imo_c' and
            tv1.outlier=false and tv2.outlier=false and tv2.outlier=false
                        order by tv1.tstamp
                        limit 1000
  """
  
  awhere = "where "+alias[0]+".code=\'"+vars[0]+"\' "
  if filter_outlier:
    awhere += " and "+alias[0]+".outlier=false\n"
  for a, v in zip(alias[1:], vars[1:]):
    awhere+=" and "+a+".code=\'"+v+"\'"
    if filter_outlier:
      awhere+=" and "+a+".outlier=false\n "
  
  
  if('afrom' in kwargs and 'ato' in kwargs):
    awhere += " and "+alias[0]+".\"tstamp\" BETWEEN \'"+ str(kwargs['afrom']) +"\' AND \'"+ str(kwargs['ato']) + "\' "
  
  
  orderby = " order by "+alias[0]+".tstamp"
  
  if("limit" in kwargs):
    limit = "\n limit "+str(kwargs['limit'])
  else:
    limit = ""
  
    
  return aselect+afrom+awhere+orderby+limit  

if __name__ == '__main__':
  
  varnames = ["CPU_C", "mirror_cell_C", "temp_imo_c", "nice_battery"]
  print(generateDSQuery(varnames))
  
  
  