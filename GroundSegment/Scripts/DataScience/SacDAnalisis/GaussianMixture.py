'''
Created on 24-jul-2021

@author: Pablo
'''
from struct import unpack
from datetime import timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sklearn.decomposition import PCA
from matplotlib import colors as mcolors
import random

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

def getColorNames(wred):
  colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
  by_hsv = [name for name, color in colors.items()]
  color_names = [name for name in by_hsv if len(name)>1]
  if not wred:
    color_names.remove('red')
  
  random.shuffle(color_names)
  return color_names

def getColorNames2(wred):

  color_names = ['blue', 'cyan', 'magenta', 'black', 'darkgreen', 'slategrey', 'navy', 'indigo',
                 'teal', 'gold', 'dimgrey', 'maroon', 'peru', 'olive', 'skyblue', 'darkviolet', 
                 'seagreen', 'darkblue', 'darkorange', 'violet', 'fuchsia', 'red']
  if not wred:
    color_names.remove('red')
  
  return color_names

def getColor(cluster, wred):
  colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
  by_hsv = [name for name, color in colors.items()]
  color_names = [name for name in by_hsv if len(name)>1]
  if not wred:
    color_names.remove('red')
  
  random.shuffle(color_names)
  return color_names[cluster]
  
def n_components_plot(X):
  n_components = np.arange(1, 21)
  models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X)
            for n in n_components]

  plt.plot(n_components, [m.bic(X) for m in models], label='BIC')
  plt.plot(n_components, [m.aic(X) for m in models], label='AIC')
  plt.legend(loc='best')
  plt.xlabel('n_components');
  plt.show()
  
def getBestGMM(X):
    lowest_bic = np.infty
    bic = []
    n_components = np.arange(1, 20)
    covariance_types = ['full', 'tied', 'diag', 'spherical']
    for cv_type in covariance_types:
        for n_c in n_components:
            # Fit a Gaussian mixture with EM
            gmm = GaussianMixture(n_components=n_c,
                                          covariance_type=cv_type, random_state=0)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm

    return best_gmm

def n_components(X):
  n_components = np.arange(1, 20)
  models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X) for n in n_components]
  
  min_val = models[0].bic(X)
  result = models[0].n_components
  for m in models[1:]:
    bx = m.bic(X)
    if bx<min_val:
      result  = m.n_components  
      min_val = bx
      
      
  return result

def draw3DPrincipalComponentPlot(X, Y, thresh):
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  msize = 16
  
  X['marker'] = ["x" if v < thresh else "v" for v in X['scores']]
  X['size'] =   [msize**2 if v < thresh else msize for v in X['scores']]
  
  colors_names = getColorNames2(False)
  colors = []
  for v, s in zip(X['cluster'],X['scores']):
    if s<thresh:
      colors.append('red')
    else:
      colors.append(colors_names[v])
    
  
  X['colors'] = colors
  #sobre escribo falsos positivos
  for k,d in X.groupby(['cluster', 'anomaly']):
      ax.scatter(d['PC1'], d['PC2'], d['PC3'], c=d.iloc[0]['colors'], label="Cluster "+str(k), s=d.iloc[0]['size'] , marker=d.iloc[0]['marker']);
      #ax.scatter(d['attempts'], d['success'], label=k)
  #df.groupby(['col5', 'col2']).size()
  Y['marker'] = ["x" if v < thresh else "o" for v in Y['scores']]
  Y['size'] =   [msize**2 if v < thresh else msize for v in Y['scores']]
  Y['colors'] = ['red' if v < thresh else 'lime' for v in Y['scores']]
  for k,d in Y.groupby(['cluster', 'anomaly']):
      ax.scatter(d['PC1'], d['PC2'], d['PC3'], c=d.iloc[0]['colors'], label="Cluster "+str(k), s=d.iloc[0]['size'] , marker=d.iloc[0]['marker']);
  
  
  plt.show()
 
 
if __name__ == '__main__':
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)
  
  df = pd.read_csv("LowOrbitSatelliteWithEclipses.csv", index_col='datetime')
  ccantPanels     = 24
  #TODO: Hacer DBScan
  columns = ['vBatAverage', 
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
             'cInEclipse',  
             'elapsedTime',
             ]
  for i in range(ccantPanels):
    columns.append("V_MODULE_"+str(i+1)+"_SA")
  

  #Aca se comenta estas linea para cambiar la cantidad de features en el test
  #Solo 2
  features = ['V_MODULE_24_SA', 'vBatAverage']
  #Solo datos del satelite(38)
  #features  = [column for column in columns if not column in ['cInEclipse','elapsedTime']]  
  #Todos los datos
  #features     = columns
  
  
  #Las 28!
  """
  features     = [column for column in columns if not column in ['BatteryEmergency',
                                                                 'IInEclipse', 
                                                                 'BatterySaveMode',
                                                                 'BatteryOvertemp',
                                                                 'BatteryOvervoltage',
                                                                 'BatteryUndervoltage',
                                                                 'BatteryOvertemperature', 
                                                                 'bvrCycle',
                                                                 'cInEclipse',
                                                                 'elapsedTime',]]
  
  
  """
  print("Amount features: ", len(features), "features: ", features)
  drawPlot = len(features)==2
  
  #Si va con principal components y cuantos
  withPCA     = False;
  scaler      = False
  n_components = 6
    
  anormal_feature = 'V_MODULE_24_SA'
  testpercent = 0.2
  
  
  df.index = pd.to_datetime(df.index)
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  #iLoc=>rows and columns
  limitData = True
  if(limitData):
    afrom = df.index[0]
    ato   = afrom+timedelta(days=2)
    df    = df.loc[(df.index>afrom) & (df.index<ato)] 
    #df = df.iloc[0:12000]
  
  #We artificially and slowly modify the value of a solar panel to break correlations. 
  #Unfortunately there is no telemetry dataset with documented errors.
  withAnomaly = True
  if withAnomaly:
    tt = round(len(df)*(testpercent/4))
    for i in range(1,tt):
      df.iloc[-i, df.columns.get_loc(anormal_feature)] = 129
    val = 128
    while(val<220):
      df.iloc[-i, df.columns.get_loc(anormal_feature)] = val
      val=val+1
      i=i+1
  
  print("Start and end dates: ", df.iloc[[0, -1],[0]])
  
  if scaler:
    dff = df[features]
    z = StandardScaler()
    dff = z.fit_transform(dff)
  else:
    dff = df
 
  if len(features)>5 and withPCA:
    
    columns = []
    pca = PCA(n_components=n_components)
    principalComponents = pca.fit_transform(dff)
    for i in range(1, n_components+1):
      columns.append("PC"+str(i))
    
    dff = pd.DataFrame(data = principalComponents
             , columns = columns)
  else:  
    dff = pd.DataFrame(data = dff, columns = features)
  featuresCount = len(dff.columns)
  train, test = train_test_split(dff, shuffle=False, test_size=testpercent)
  gmm = getBestGMM(train)
  labels = gmm.predict(train)
  probs = gmm.predict_proba(train)
  
  
  
  print("Score: ", silhouette_score(train, labels))
  print("n_components: ", gmm.n_components)
  print("covariance_type: ", gmm.covariance_type)
  
  
  scores = gmm.score_samples(train)
  thresh =  scores.min()
  print("Minimun score:", thresh)
  
  anomalies =  scores[scores<thresh]
  train['anomaly'] = [1 if v < thresh else 0 for v in scores]
  train['scores']   = scores
  
  print("Anomalies in train: ", len(anomalies))
  
  
  scoresTest      = gmm.score_samples(test)
  test['anomaly'] = [1 if v < thresh else 0 for v in scoresTest]
  test['scores']  = scoresTest
  anomaliesTest   = scoresTest[scoresTest<thresh]
  print("Anomalies in test: ", len(anomaliesTest))
  
  train['cluster']  = labels
  test['cluster']   = -1
  
  """
  #It's not working
  if drawPlot and not withPCA:
    fig=plt.figure(figsize=(8,6))   
    dftrain = pd.DataFrame(data=train, columns=features)
    dftrain['cluster'] = labels
    mscores =  ['x' if v < thresh else 'v' for v in scores]
    mcolors =  ['r' if v < thresh else 'b' for v in scores]
    #fig=plt.figure(figsize=(10,10))   
    size = 50 * probs.max(1) ** 2 # square emphasizes differences
    for k,d in dftrain.groupby('cluster'):
        plt.scatter(d[features[0]], d[features[1]], label="Cluster "+str(k), cmap='viridis');
        #ax.scatter(d['attempts'], d['success'], label=k)
    
    plt.xlabel('Normalized Panel 24 current');
    plt.ylabel('Normalized elapsedTime');
    plot_gmm(gmm, train, labels)
    plt.legend()
    plt.grid(True)
  """
  #Componentes principales
  if withPCA and featuresCount<4:
    draw3DPrincipalComponentPlot(train, test, thresh)   
    
    
    
  #plt.close()
  #plt.figure().clear()
  
  #scores = gmm.score_samples(test)
  #anomalies =  scores[scores<thresh]
  #print("Total Anomalies: ", len(anomalies))
  
  """
  if drawPlot and not withPCA:
    fig=plt.figure(figsize=(8,6)) 
    dftest = pd.DataFrame(data=test, columns=features)
    size = 50 * probs.max(1) ** 2 # square emphasizes differences
    #plt.scatter(train[:, 0], train[:, 1], c=labels, cmap='viridis', s=size);
    dftest['label'] = ['Test Anomaly' if v < thresh else 'Test Nominal' for v in scores]
    dftest['color'] = ['r' if v < thresh else 'b' for v in scores]
    dftest['mark'] =  ['x' if v < thresh else 'v' for v in scores]
    for k,d in dftest.groupby('label'):
        plt.scatter(d[features[0]], d[features[1]], label=k, c=d.iloc[0]['color'], marker=d.iloc[0]['mark'], cmap='viridis');
     
    
    #plt.scatter(test[:, 0], test[:, 1], marker='x', color=mcolors, cmap='viridis');
    plt.xlabel('Normalized Panel 24 current');
    plt.ylabel('Normalized elapsedTime');
    plt.legend()
    #plt.scatter(values[:,0], values[:,1], marker='x', color='r')
    #plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
    plot_ellipse(gmm)
    plt.show()
  #['datetime', 'vBatAverage', 'IInEclipse', 'BatteryDischarging', 'bvrCycle']
  """
  
  print("stop")
  
  