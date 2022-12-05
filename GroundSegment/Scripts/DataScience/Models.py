'''
Created on 17-mar-2021

@author: pabli
'''
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

def PolinomialRegresionModel(df, xvalues, yvalue):
  
  X = df[xvalues]
  y = df[yvalue]
  #Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
  X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X, y, test_size=0.2)
  
  poli_reg = PolynomialFeatures(degree = 4)
  X_train_poli = poli_reg.fit_transform(X_train_p)
  X_test_poli = poli_reg.fit_transform(X_test_p) 
  
  #Defino el algoritmo a utilizar

  pr = linear_model.LinearRegression()
  #Entreno el modelo
  pr.fit(X_train_poli, y_train_p)
  Y_pred_pr = pr.predict(X_test_poli)
      
  
  #plt.scatter(X_test_p, y_test_p)
  #plt.plot(X_test_p, Y_pred_pr, color='red', linewidth=3)
  #plt.show()
  print('Precision del modelo:')
  print(pr.score(X_train_poli, y_train_p))
