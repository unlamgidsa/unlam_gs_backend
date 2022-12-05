'''
Created on 27-jul-2021

@author: pabli
'''
import os, sys, glob 
import time
from struct import unpack
from datetime import datetime, timedelta
from Scripts.DSUtils import getProjectPath
import sys; 
#print('%s %s' % (sys.executable or sys.platform, sys.version))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'GroundSegment.settings'; 

import struct
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib as mpl
import pytz
colors = ['navy', 'turquoise', 'darkorange']

"""
def make_ellipses(gmm, ax):
    for n, color in enumerate(colors):
        if gmm.covariance_type == 'full':
            covariances = gmm.covariances_[n][:2, :2]
        elif gmm.covariance_type == 'tied':
            covariances = gmm.covariances_[:2, :2]
        elif gmm.covariance_type == 'diag':
            covariances = np.diag(gmm.covariances_[n][:2])
        elif gmm.covariance_type == 'spherical':
            covariances = np.eye(gmm.means_.shape[1]) * gmm.covariances_[n]
        v, w = np.linalg.eigh(covariances)
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan2(u[1], u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
                                  180 + angle, color=color)
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(0.5)
        ax.add_artist(ell)
        ax.set_aspect('equal', 'datalim')
"""

def draw_ellipse(position, covariance, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    # Draw the Ellipse
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))
        
def plot_gmm(gmm, X, labels, label=True, ax=None):
    ax = ax or plt.gca()
    
    #labels = gmm.fit(X).predict(X)
    if label:
        ax.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis', zorder=2)
    else:
        ax.scatter(X[:, 0], X[:, 1], s=40, zorder=2)
    ax.axis('equal')
    
    w_factor = 0.8 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covariances_, gmm.weights_):
        #draw_ellipse(pos, covar, alpha=0.5, visible=True, color='green')
        draw_ellipse(pos, covar, alpha=w * w_factor, visible=True, color='green')

def plot_ellipse(gmm):
    w_factor = 1 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covariances_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor, visible=True, color='green')
        #draw_ellipse(pos, covar, alpha=0.5, visible=True, color='green')

def is_set(x, n):
    return x & 2**n != 0 
  


def loadFromDB():  
  import django
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()
  from Telemetry.models.TlmyRawData import TlmyRawData
  from GroundSegment.models.Satellite import Satellite
  from Telemetry.models.FrameType import FrameType
  from GroundSegment.models.Satellite import Satellite
  from Telemetry.models.TlmyRawData import TlmyRawData

  sat = Satellite.objects.get(code="SAC-D") 
  ato   = datetime(2016, 1, 1, 0, 0, 0, tzinfo=pytz.UTC) 
  raws = TlmyRawData.objects.filter(satellite=sat, pktdatetime__lte=
                                    ato).order_by('pktdatetime')#[0:5000]
  PCSBase = 1604
  
  ccantPanels     = 24
  bvBatAverage    = PCSBase+750
  bBatState       = PCSBase+46 #<=El 5 es batery discharging
  bV_MODULE       = PCSBase+672
  #bSP_MMB2_1      = PCSBase+643 
  bISenseRS1      = PCSBase+670
  bISenseRS2      = PCSBase+671
  #bIdMinor        = PCSBase+755
  #bTEMP_1A_HSC    = PCSBase+755+1
  bstatusPCS2     = PCSBase+1
  #bSP_ACEA_A_1    = PCSBase+70
  bvrCycle        = PCSBase+47
  ff = []
  
  for r in raws:
    
    binary = r.getBlob()
    llist = [
       r.pktdatetime,
       struct.unpack(">H", binary[bvBatAverage:bvBatAverage+struct.calcsize("H")])[0]*0.01873128+-38.682956,#vBatAverage
       is_set(struct.unpack("B", binary[bstatusPCS2:bstatusPCS2+struct.calcsize("B")])[0],2),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],0),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],1),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],2),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],3),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],4),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],5),
       is_set(struct.unpack("B", binary[bBatState:bBatState+struct.calcsize("B")])[0],6),
       struct.unpack("B", binary[bvrCycle:bvrCycle+struct.calcsize("B")])[0],
       struct.unpack("B", binary[bISenseRS1:bISenseRS1+struct.calcsize("B")])[0],
       struct.unpack("B", binary[bISenseRS2:bISenseRS2+struct.calcsize("B")])[0],
      ]
    
    for i in range(ccantPanels):
      llist.append(struct.unpack("B", binary[bV_MODULE:bV_MODULE+struct.calcsize("B")])[0])
      bV_MODULE+=1
    bV_MODULE       = PCSBase+672
    
    ff.append(tuple(llist))
    
    ##print(ff[len(ff)-1])
    
  columns = ['datetime', 
             'vBatAverage', 
             'IInEclipse', 
             'BatteryEmergency',
             'BatterySaveMode',
             'BatteryOvertemp',
             'BatteryOvervoltage',
             'BatteryUndervoltage',
             'BatteryDischarging',
             'BatteryOvertemperature', 
             'bvrCycle',
             'ISenseRS1',
             'ISenseRS2',
             ]
  for i in range(ccantPanels):
    columns.append("V_MODULE_"+str(i+1)+"_SA")
    
  df = pd.DataFrame(ff, columns = columns)#, , index_col='datetime'
  df.to_csv("./SACD.csv")
  return df
  