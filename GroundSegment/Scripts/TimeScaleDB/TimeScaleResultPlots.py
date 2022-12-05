'''
Created on 10 jun. 2020

@author: pablo
'''
#source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
#python /home/pablo/git/GroundSegment/GroundSegment/Scripts/TimeScaleDB/TimeScaleResultPlots.py

from numpy.random.mtrand import randint
import os, sys
import numpy as np
from django.db.models.fields import IntegerField

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#proj_path = '/home/psoligo/git/GroundSegment/GroundSegment/'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


#loadDjangoApp()
from GroundSegment.models.Log import Log
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
#TI-NORMTABLE TI-HIPERTABLE SE-HIPERTABLE SE-NORMTABLE
from django.db.models import Q
from django.db.models.functions import Cast

if __name__ == '__main__':
    
    lw = 8
    styles = ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 
              'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 
              'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 
              'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 
              'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
    1
    
    #ss = styles[randint(len(styles))]
    ss = 'bmh'
    mpl.style.use(ss)
    print("Style, ", ss);
    
    gradpol = 5
    afromcr = int(sys.argv[1])
    atocr   = int(sys.argv[2])
    cantidadreg = "Cantidad de registros (En millones)"
    seg         = "Segundos/Consulta o inserción "
    
    ##value = Value.objects.annotate(as_float=Cast('integer', FloatField())).get()> 
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-NORMTABLENN", cr__gt=afromcr, cr__lt=atocr).order_by('id')
    normalinsertsy   = list(map(lambda val:float(val), qs.values_list('description', flat="True" )))
    normalinsertsx   = list(map(lambda val:int(val)/1000000, qs.values_list('module', flat="True" )))
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-HIPERTABLENN",cr__gt=afromcr, cr__lt=atocr).order_by('id')
    hiperinsertsy    =  list(map(lambda val:float(val), qs.values_list('description', flat="True" )))
    hiperinsertsx    =  list(map(lambda val:int(val)/1000000, qs.values_list('module', flat="True" )))
    
    pf  = np.polyfit(normalinsertsx, normalinsertsy, gradpol)
    pfn = np.poly1d(pf)
    
    pf  = np.polyfit(hiperinsertsx, hiperinsertsy, gradpol)
    pfh = np.poly1d(pf)
    
    plt.plot(normalinsertsx, normalinsertsy,'ro', label='Tabla Regular');
    plt.plot(hiperinsertsx, hiperinsertsy, 'bo', label='Hipertabla');
    
    plt.plot(normalinsertsx, pfn(normalinsertsx), 'r', linewidth=lw, label='Tabla regular - Polyfit');
    plt.plot(hiperinsertsx, pfh(hiperinsertsx), 'b', linewidth=lw, label='Hypertabla - Polyfit');
    plt.title(label="Tiempo medio para inserciones en tabla e hipertabla")
    plt.xlabel(cantidadreg)
    plt.ylabel(seg)
    plt.legend()
    plt.show()
    
    
       
    
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-HIPERTABLENN", cr__gt=afromcr, cr__lt=atocr).order_by('id')
    hiperqy         = list(map(lambda val:float(val),qs.values_list('description', flat="True" )))
    hiperqx         = list(map(lambda val:int(val)/1000000,qs.order_by('id').values_list('module', flat="True" )))
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-NORMTABLENN", cr__gt=afromcr, cr__lt=atocr).order_by('id')
    normalqy          = list(map(lambda val:float(val),qs.values_list('description', flat="True" )))
    normalqx          = list(map(lambda val:int(val)/1000000,qs.values_list('module', flat="True" )))
    
    
    pf  = np.polyfit(normalqx,  normalqy, gradpol)
    pfn = np.poly1d(pf)
    
    pf  = np.polyfit(hiperqx, hiperqy , gradpol)
    pfh = np.poly1d(pf)
    
    
    plt.plot(normalqx, normalqy,  'ro', label='Tabla Regular');
    plt.plot(hiperqx, hiperqy, 'bo', label='Hipertabla');
    
    plt.plot(normalqx , pfn(normalqx ), 'r', linewidth=lw, label='Tabla regular - Polyfit');
    plt.plot(hiperqx, pfh(hiperqx), 'b', linewidth=lw, label='Hypertabla - Polyfit');
        
    plt.title(label="Consultas tiempo real en tabla e hipertabla")
    plt.xlabel(cantidadreg)
    plt.ylabel(seg)
    plt.legend()
    plt.show()
    
    
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-HISTHIPERTABLENN", cr__gt=afromcr, cr__lt=atocr)
    histhiperqy         = list(map(lambda val:float(val),qs.order_by('id').values_list('description', flat="True" )))
    histhiperqx        = list(map(lambda val:int(val)/1000000,qs.order_by('id').values_list('module', flat="True" )))
    
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-HISTNORMTABLENN", cr__gt=afromcr, cr__lt=atocr)
    histnormalqy          = list(map(lambda val:float(val),qs.order_by('id').values_list('description', flat="True" )))
    histnormalqx          = list(map(lambda val:int(val)/1000000,qs.order_by('id').values_list('module', flat="True" )))
       
    
    pf  = np.polyfit(histnormalqx,  histnormalqy, gradpol)
    pfn = np.poly1d(pf)
    
    pf  = np.polyfit(histhiperqx, histhiperqy , gradpol)
    pfh = np.poly1d(pf)
          
    plt.plot(histnormalqx, histnormalqy, 'ro', label='Tabla Regular');
    plt.plot(histhiperqx, histhiperqy, 'bo', label='Hipertabla');
    
    plt.plot(histnormalqx , pfn(histnormalqx), 'r', linewidth=lw, label='Tabla regular - Polyfit');
    plt.plot(histhiperqx, pfh(histhiperqx), 'b', linewidth=lw, label='Hypertabla - Polyfit');
    
    plt.title(label="Consultas historicas en tabla e hipertabla")
    plt.xlabel(cantidadreg)
    plt.ylabel(seg)
    plt.legend()
    plt.show()
    
    
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-AGRHIPERTABLENN", cr__gt=afromcr, cr__lt=atocr).order_by('id')
    agrhiperqy        = list(map(lambda val:float(val),qs.values_list('description', flat="True" )))
    agrhiperqx        = list(map(lambda val:int(val)/1000000,qs.values_list('module', flat="True" )))
    
    qs = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code__contains="SE-AGRNORMALTABLENN", cr__gt=afromcr, cr__lt=atocr).order_by('id')
    agrnormalqy          = list(map(lambda val:float(val),qs.values_list('description', flat="True" )))
    agrnormalqx          = list(map(lambda val:int(val)/1000000,qs.values_list('module', flat="True" )))
       
    
    pf  = np.polyfit(agrnormalqx,  agrnormalqy, gradpol)
    pfn = np.poly1d(pf)
    
    pf  = np.polyfit(agrhiperqx, agrhiperqy , gradpol)
    pfh = np.poly1d(pf)
          
    plt.plot(agrnormalqx, agrnormalqy, 'ro', label='Tabla Regular');
    plt.plot(agrhiperqx,agrhiperqy, 'bo', label='Hipertabla');
    
    plt.plot(agrnormalqx , pfn(agrnormalqx), 'r', linewidth=lw, label='Tabla regular - Polyfit');
    plt.plot(agrhiperqx, pfh(agrhiperqx), 'b', linewidth=lw, label='Hypertabla - Polyfit');
    
    plt.title(label="Consultas agregadas historicas en tabla e hipertabla")
    plt.xlabel(cantidadreg)
    plt.ylabel(seg)
    plt.legend()
    plt.show()
    
    print("Fin plots")