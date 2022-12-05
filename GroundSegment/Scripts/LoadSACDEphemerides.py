'''
Created on 17 may. 2019

@author: pablo
'''
import os, sys, glob 
import gzip
import pandas as pd

import pytz
from datetime import timezone, datetime, timedelta

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from CODS.models import Ephemeride, ReferenceSystem
from GroundSegment.models.Satellite import Satellite

if __name__ == '__main__':
    
    #delete all
    Ephemeride.objects.all().delete()
    
    
    print("Buscando ephemerides SAC-D")
    
    pathBase = "/home/psoligo/Descargas/Pending/MJ2000"  
    pathbasedest = "/home/psoligo/Descargas/Processed/MJ2000"  
    
    
    #pathBase = "/home/pablo/Descargas/Ephem/Pending/MJ2000"  
    #pathbasedest = "/home/pablo/Descargas/Ephem/Processed/MJ2000"  
    pathfile = pathBase+"/*.gz"   
    print("Buscando en...", pathfile )
    #*HEADER SAC-D        2879 XYZ        UTC        MJ2K       PRO        37673 11024A      CONAE      2014/01/28 18:29:24
    #2013/11/17 00:01:00.00000000    4723.172123   -2394.509503   -4637.288636   3.7144796792  -3.4366645656   5.5630101162
    #filename = '/home/pablo/Descargas/Ephem/Pending/MJ2000/CODS_20131102_135727_SACD_ORBEPHEM_MJ2K_XYZ_O.TXT.gz'
    
    #hardcode for now
    rs  = ReferenceSystem.objects.get(code="MJ2K")
    sat = Satellite.objects.get(code="SACD")
    
    mydateparser = lambda x: pd.datetime.strptime(x, "%Y/%m/%d %H:%M:%S")
   
    #2013/10/30 13:50:00.00000000
    #dateparse = lambda x: pd.datetime.strptime(x, '%Y/%m/%d %H:%M:%S')
    try:
    
        for filename in glob.glob(pathfile):
            #Tengo que transformar los 24:00:00 en el dia siguiente
            
            
                       
            ds = pd.read_fwf(filename, compression='gzip', widths=[19,9,15,15,15,15,15,15], skiprows=0)
            #, parse_dates=[0], date_parser=mydateparser
            
            ds.columns = ['epoch', 'None', 'x', 'y', 'z', 'x.', 'y.', 'z.']
            
    
            for index, row in ds.iterrows():
                try:
                    epoch = datetime.strptime(row['epoch'], "%Y/%m/%d %H:%M:%S").replace(tzinfo=pytz.UTC)
                except Exception as ex:
                    #Fecha con formato 24:00:00
                    ls = list(row['epoch'])
                    ls[11] = '0'
                    ls[12] = '0'
                    
                    epoch = datetime.strptime("".join(ls), "%Y/%m/%d %H:%M:%S").replace(tzinfo=pytz.UTC) + timedelta(days=1)
                    
                    
                
                ep, created = Ephemeride.objects.get_or_create(satellite=sat, referenceSystem=rs, epoch=epoch)
                
                
                    
                    
                
                    
                #ep.epoch            = row['epoch']
                #ep.referenceSystem  = rs
                #ep.satellite        = sat
                ep.x                = row['x']
                ep.y                = row['y']
                ep.z                = row['z']
                ep.xp               = row['x.']
                ep.yp               = row['y.']
                ep.zp               = row['z.']
                #override because the default value cause problems
                ep.epoch            = epoch
                
                if(created):
                    pass                
                else:
                    print("Objeto ya creado!", ep.epoch)
                
                ep.save()
            
            print("Fin de archivo, se muevo a destino final")
            path, fn = os.path.split(filename)
            os.rename(filename, pathbasedest+'/'+fn)        
            
            
        
        
    except Exception as ex:
        print("Error in file", ex)
   