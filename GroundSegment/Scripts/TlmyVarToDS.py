'''
Created on 16-jun-2021

@author: pabli
'''


import os; 
from Scripts.DSUtils import getProjectPath, generateDSQuery
from datetime import datetime
import pandas as pd
from django.db import connection

if __name__ == '__main__':
    varnames = ["CPU_C", "mirror_cell_C", "temp_imo_c", "nice_battery"]
    
    afrom = datetime(2020, 10, 5, 0, 0, 0) 
    ato   = datetime(2020, 11, 1, 0, 0, 0)
  
    query = generateDSQuery(vars=varnames, afrom=afrom, ato=ato)
    print(query)
    df = pd.read_sql_query(sql=query, con=connection)
    print(df.head())
    
    