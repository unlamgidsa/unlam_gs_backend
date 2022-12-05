'''
Created on 26 oct. 2020

@author: pablo
'''

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


    g1afromcr = 450000000 
    g1atocr   = 650000000
    
    g2afromcr = 1010000000
    g2atocr   = 1060000000
    
    #amount 50
    #process 3
    
    
    cantidadreg = "Cantidad de registros (En millones)"
    seg         = "Segundos/Consulta o inserción "
    
    g1nt = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-NORMTABLENN", 
                                                                          cr__gt=g1afromcr, cr__lt=g1atocr).order_by('id')
    
    g2nt = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-NORMTABLENN", 
                                                                          cr__gt=g2afromcr, cr__lt=g2atocr).order_by('id')
                                                                          
                                                                          
    g1normalinsertsy   = list(map(lambda val:float(val), g1nt.values_list('description', flat="True" )))
    g1nttt = [val*7500*3*4 for val in g1normalinsertsy]
    
    g2normalinsertsy   = list(map(lambda val:float(val), g2nt.values_list('description', flat="True" )))
    g2nttt = [val*7500*3*4 for val in g2normalinsertsy]
    
    
    
    #----------------------------------------------------
    
    
    g1ht = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-HIPERTABLENN", 
                                                                          cr__gt=g1afromcr, cr__lt=g1atocr).order_by('id')
    
    g2ht = Log.objects.annotate(cr=Cast('module', IntegerField())).filter(code="TI-HIPERTABLENN", 
                                                                          cr__gt=g2afromcr, cr__lt=g2atocr).order_by('id')
                                                                          
                                                                          
    g1hyperinsertsy   = list(map(lambda val:float(val), g1ht.values_list('description', flat="True" )))
    g1httt = [val*7500*3*4 for val in g1hyperinsertsy]
    
    g1hyperinsertsy   = list(map(lambda val:float(val), g2ht.values_list('description', flat="True" )))
    g2httt = [val*7500*3*4 for val in g1hyperinsertsy]
    
    print("Sumas", sum(g1nttt), sum(g1httt), sum(g2nttt), sum(g2httt))
    print("Sumas", sum(g1nttt)-sum(g1httt), sum(g2nttt)-sum(g2httt))
    
    
    print("Fin plots")