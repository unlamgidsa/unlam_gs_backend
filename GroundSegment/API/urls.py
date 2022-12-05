'''
Created on 7 jul. 2018

@author: pablo
'''


from django.urls import re_path
from .views import  ParameterViewSet
from .views import SatelliteListView

from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from API.views import TlmyVarList,TlmyDictionaryView, UserItemView, CustomAuthToken,\
    UserItemCreateView, GetLastTelemetryTimeStamp, TlmyRawDataView, WSTest
from GroundSegment.models.UserItem import UserItem

"""-----------------API URLS---------------------------"""
"""
http://127.0.0.1:8000/TlmyRawData/
En authorization
username:
password:
{
    "capturedAt": "2022-03-16T00:00:00",
    "pktdatetime": "2022-03-16T00:00:00",
    "source": "RTSatellite",
    "strdata": "RTSatellite",
    "realTime": false,
    "tag": "EMU_RTSatellite"
}
--------------------------------------------------------
http://127.0.0.1:8000/API/api-token-auth/
En Body
username y password
--------------------------------------------------------
http://127.0.0.1:8000/API/SatelliteList
token en headers
"key":"Authorization",
"value":"Token 1111111111111",

http://127.0.0.1:8000/API/TlmyVarDict/TITA
token en headers
"key":"Authorization",
"value":"Token 1111111111111",

http://127.0.0.1:8000/API/TlmyVarList/TITA.CPU_C/647414533287/1647436133287
token en headers
"key":"Authorization",
"value":"Token 1111111111111",
"""
"""----------------------------------------------------"""


router = DefaultRouter()
#Cambie base_name por basename, verificar la razon del problema
try:
    router.register(r'Parameters', ParameterViewSet, basename='Parameter')
except:
    router.register(r'Parameters', ParameterViewSet, base_name='Parameter')
    
#urlpatterns = router.urls

urlpatterns = [
    #Comprobado que es usada por openmct para pedir lista de satelites
    re_path(r'^SatelliteList', SatelliteListView.as_view() , name='SatelliteListView'),
    re_path(r'^', include(router.urls)),

    
    #Comprobado que es usada por el openmct para pedir los valores de las variables de telemetri
    path('TlmyVarList/<str:sat_tlmyId>/<str:afrom>/<str:ato>', TlmyVarList.as_view()),
    #Misma url sin desde hasta
    path('TlmyVarList/<str:sat_tlmyId>/', TlmyVarList.as_view()),
    
    #Comprobado que es usada por el openmct para pedir la lista de tipos de variable de telemetria
    path('TlmyVarDict/<str:satellite>', TlmyDictionaryView.as_view()),
    path('UserItems', UserItemView.as_view()),
    path('UserItems/Create', UserItemCreateView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    
    #http://127.0.0.1:8000/API/wstest/
    path('wstest/', WSTest.as_view()),
   
    #http://localhost:8000/API/TlmyVarDict/FS2017
    
    
    #Existe raw data para esta fecha y satelite?
    path('TlmyRawData/<str:satellite>/<str:adatetime>', TlmyRawDataView.as_view()),
    
    
    #http://localhost:8000/API/GetLastTelemetryTimeStamp/TITA
    path('GetLastTelemetryTimeStamp/<str:satellite>', GetLastTelemetryTimeStamp.as_view()),
    
    
    
    
    
    #Open MCT: http://localhost:8080/history/fs2017.BattV?start=1536153300189&end=1536154200189
    
    #url(r'^TlmyVarTypeList/(<int:satellite_id>)/(<int:tlmyVarType_id>)/$', TlmyVarTypeListView.as_view() , name='TlmyVarTypeListView'),
]
