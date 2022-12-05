'''
Created on 15 may. 2018

@author: pablo
'''
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
#from django.http import Http404
from rest_framework.generics import CreateAPIView, ListAPIView,\
    get_object_or_404, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import DjangoModelPermissions , IsAdminUser
from API.Serializers import TlmyRawDataSerializer, SatelliteSerializer,\
    TlmyVarTypeSerializer, ParameterSerializer, UserItemCreateSerializer
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.models.TlmyVar import TlmyVar
from GroundSegment.models.Satellite import Satellite
from django.db.utils import IntegrityError
from django.http import JsonResponse, Http404
from rest_framework.exceptions import APIException
from django.db.models.query import QuerySet
from Telemetry.models.TlmyVarType import TlmyVarType
from GroundSegment.models.Parameter import Parameter
from Telemetry.tasks import TlmyDecode
from GroundSegment import settings
from Calibration import *
from .Serializers import MCTTelemetrySerializer,TlmyDictionarySerializer
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from GroundSegment.models.UserItem import UserItem
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.db.models import Q
import pytz
from django.db import IntegrityError, transaction
class WSTest(TemplateView):
  template_name = "wstest.html"

class CustomAuthToken(ObtainAuthToken):
    """
        http://127.0.0.1:8000/API/api-token-auth/
        body:
        {
            "username": "sa",
            "password": "el_password_de_sa"    
        }
    """
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username  = serializer.validated_data['username']
        password = serializer.validated_data['password']
        #token, created = Token.objects.get_or_create(user=user)
        #curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
        try:
            user  = User.objects.get(username=username)
            #token = Token.objects.create(user=user)
            #Esto parece ser innecesario.
            #if not user.check_password(password):
            #    return HttpResponse('Unauthorized-Invalid password', status=401)
            
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        except Token.DoesNotExist:
            return HttpResponse('Unauthorized', status=401)
            
        
       

class DataExists(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Data already exists'
    default_code = 'data_exists'
    
    
class MCTTelemetry(object):
    
    def __init__(self, timestamp, value, aid, amax, amin, aformat):
        self.timestamp   = int(timestamp)
        self.value       = value
        self.id          = aid
        self.max         = amax
        self.min         = amin
        
        #if(aformat==TlmyVarType.FLOAT):        
        #    self.format      = "float"
class TValue():
    def __init__(self, *args, **kwargs):
        self.key    = kwargs['key']
        self.name   = kwargs['name']
        self.format = kwargs['format']

        if('units' in kwargs):
            self.units = kwargs['units']

        if('max' in kwargs):
            self.max = kwargs['max']
                
        if('min' in kwargs):
            self.min = kwargs['min']

        if('source' in kwargs):
            self.source = kwargs['source']

        self.hints = kwargs['hints']

class TlmyDictionary():
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.key  = kwargs['key']
        self.measurements = []
    
class TMeasurament():
    def __init__(self, *args, **kwargs):
        self.name       = kwargs['name']
        self.key        = kwargs['key']
        self.values     = kwargs['values']
    
class THint():
    def __init__(self, *args, **kwargs):
        if('range' in kwargs):
            self.range    = kwargs['range']

        if('domain' in kwargs):
            self.domain   = kwargs['domain']
            
          


class UserItemCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication] #, SessionAuthentication
    permission_classes  =   [IsAdminUser]#[AllowAny] 
    #queryset            =   UserItem.objects.all()
    model               =   UserItem
    serializer_class    =   UserItemCreateSerializer
    
    #def get_queryset(self):
    #    return UserItem.objects.filter(owner=self.request.user)
    def post(self, request):
        try:
            user = User.objects.get(username=self.request.user.username)           
            
            if user.items.count()>0:
                it = user.items.all()[0]
                it.jsonf = request.data['jsonf'] 
                it.save()
                return Response("Updated", status=status.HTTP_202_ACCEPTED)
            else:
                serializer = UserItemCreateSerializer(data=request.data)
                if serializer.is_valid():
                    instance = serializer.save(owner=self.request.user) #user=user
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            data = {"error": True, "errors": ex.__str__(),}
            return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)   
             
            
class UserItemView(APIView):
    authentication_classes = [TokenAuthentication] #, SessionAuthentication
    permission_classes = [IsAuthenticated]#[AllowAny]# 
    
    
    def get(self,request):
    
        uts = UserItem.objects.filter(owner=self.request.user)
        
            
        return Response(uts.values_list('jsonf', flat=True))
    
    
class TlmyRawDataView(APIView):
    """
    authentication_classes = [BasicAuthentication] 
    permission_classes = [AllowAny];
    
    authentication_classes = [TokenAuthentication] #, SessionAuthentication
    permission_classes = [IsAuthenticated]#[AllowAny]# 
    
    authentication_classes = [BasicAuthentication] #, 
    permission_classes = [IsAdminUser]#[AllowAny] 
    
    """
    authentication_classes = [BasicAuthentication] #, 
    permission_classes = [IsAdminUser]#[AllowAny] 

    
    def get(self, request, satellite, adatetime, format=None):
        
        #Example
        #tstamp = datetime.strptime("2021-10-24 17:52:08.000", "%Y-%m-%d %H:%M:%S.%f").timestamp()
        #dt=datetime.fromtimestamp(tstamp, pytz.UTC)`
        #TlmyRawData.objects.filter(satellite__noradId=sat_code, pktdatetime=dt)
        
        try:
            dt=datetime.fromtimestamp(int(adatetime), pytz.UTC)
            rd = TlmyRawData.objects.get(satellite__noradId=satellite, pktdatetime=dt)
            
        except TlmyRawData.DoesNotExist:
          db_data = TlmyRawData.objects.none()
          serializer = TlmyRawDataSerializer(db_data, many=True)
          return Response(serializer.data)
          
          
        return Response(TlmyRawDataSerializer(rd).data)
    
    
         
        
class GetLastTelemetryTimeStamp(APIView):
    #authentication_classes = [SessionAuthentication] 
    #permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self,request, satellite):
        #http://localhost:8000/API/GetLastTelemetryTimeStamp/TITA
       
        sat_code   = satellite
        #print(self.request.user, self.request.auth);
        tstamp = TlmyVar.objects.filter(tlmyVarType__in = TlmyVarType.objects.filter(satellite__code=sat_code)).order_by('-tstamp')[0].tstamp
        
        return Response({"tstamp":tstamp.isoformat()})


class TlmyDictionaryView(APIView):
    
    authentication_classes = [TokenAuthentication] #, SessionAuthentication
    permission_classes = [IsAuthenticated]#[AllowAny]# 
    
     
    
    def get(self,request, satellite):
        #http://localhost:8000/API/TlmyVarDict/FS2017
        #print(self.request.user, self.request.auth);
        
        sat_code   = satellite
        #print(self.request.user, self.request.auth);
        
        lsatellite =  Satellite.objects.get(code=sat_code)
        tlmyVarTypes = lsatellite.tmlyVarType.order_by('code')

        tlmyDictionary = TlmyDictionary(key=lsatellite.code, name=lsatellite.code)

        for tlm in tlmyVarTypes:
            lvalues = [TValue(key="value", name="Value", 
                        format=TlmyVarType.VARTYPE[tlm.varType][1], units=tlm.unitOfMeasurement.code, max=tlm.maxValue, min=tlm.minValue, hints=THint(range=1)),
                        TValue(key="utc", name="TimeStamp", source="timestamp",
                        format="utc", hints=THint(domain=1)), 
                        ]
            #TlmyVarType.VARTYPE[1][1]
            ms = TMeasurament(key=tlm.satellite.code+"."+tlm.code, name=tlm.code, values=lvalues) 
            tlmyDictionary.measurements.append(ms)
        
        #serialized = TlmyDictionarySerializer(tlmyDictionary, many=False)
        return Response(TlmyDictionarySerializer(tlmyDictionary).data)



class TlmyVarList(ListAPIView):
    """
        http://127.0.0.1:8000/API/TlmyVarList/TITA.CPU_C/
        headers:
        {
            "Authorization": "Token el_token_que_corresponda",
             
        }
    """
    
    
    
    serializer_class = MCTTelemetrySerializer
    authentication_classes = [TokenAuthentication]#SessionAuthentication
    permission_classes = [IsAuthenticated]#[AllowAny]
    
    
    
        
    def get_queryset(self):
        #Original OPEN MCT->http://localhost:8080/history/fs2017.BattV?start=1536153300189&end=1536154200189
        #Lo que intento hacer->http://127.0.0.1:8000/API/TlmyVarList/FS2017.BattV/1536153300189/1536154200189
        #http://127.0.0.1:8000/API/TlmyVarList/TITA.CPU_C/1583070716183/1583158916183
        #URL propuesta->TlmyVarList/<str:sat_tlmyId>/<int:afrom>/<int:ato>
        #print(self.request.user, self.request.auth);
        
        sat_tlmyId   = self.kwargs['sat_tlmyId']
        satcode     = sat_tlmyId.split('.')[0]
        tlmycode    = sat_tlmyId.split('.')[1]
        
        _tlmyVarType = TlmyVarType.objects.get(satellite__code=satcode, code=tlmycode)
       
        if ('afrom' in self.kwargs)or('ato' in self.kwargs):
            afrom       = self.kwargs['afrom']
            ato         = self.kwargs['ato']
            afrom =  datetime.fromtimestamp(int(afrom)/1000, pytz.UTC) # float(afrom)
            ato   = datetime.fromtimestamp(int(ato)/1000, pytz.UTC)
        else:
            #Esta pidiendo el ultimo dato para este satelite...harcode ultima hora, parametrizar...
            #Obtengo el ultimo dato
            ltv = TlmyVar.objects.filter(tlmyVarType=_tlmyVarType).order_by('tstamp').last()
            if ltv!=None:
                afrom = ltv.tstamp - timedelta(minutes=10)#(ltv.tstamp-timedelta(hours=1)).timestamp()*1000
                ato   = ltv.tstamp#ltv.tstamp.timestamp()*1000
            else:
                ato     = datetime.now(utc)
                afrom   = ato-timedelta(minutes=10)
                
        
        vvars = TlmyVar.objects.filter(Q(tlmyVarType=_tlmyVarType)&Q(tstamp__range=(afrom, ato))&Q(outlier=False))\
            .order_by('tstamp')\
            .prefetch_related('tlmyVarType', 'tlmyVarType__unitOfMeasurement')
        #afrom = datetime.strptime("2015-05-01 00:00:00",'%Y-%m-%d %H:%M:%S').timestamp()*1000;
        #ato   = datetime.strptime("2018-05-02 00:00:00", '%Y-%m-%d %H:%M:%S').timestamp()*1000;
        
        
        result = []
        for var in vvars:
                        
            result.append(MCTTelemetry(var.UnixTimeStamp, 
                                       var.calSValue, 
                                       sat_tlmyId, 
                                       var.tlmyVarType.maxValue, 
                                       var.tlmyVarType.minValue,
                                       var.tlmyVarType.varType))
            
        
        return result
        
    



class TlmyRawDataList(CreateAPIView):

    serializer_class = TlmyRawDataSerializer
    authentication_classes = [BasicAuthentication] #, 
    permission_classes = [IsAdminUser]#[AllowAny] 
    
    """
    request.auth will be a rest_framework.authtoken.models.Token instance.
    
    def get(self, request, format=None):
        snippets = TlmyRawData.objects.all()[0:5]
        serializer = TlmyRawDataSerializer(snippets, many=True)
        return Response(serializer.data)
    """
    #@classmethod
    cachesats = {}
    
    task = None    
    
    @classmethod
    def get_task(cls):
        if cls.task==None:
            cls.task=TlmyDecode()
        else:
            pass
            #print("Tarea cacheada!!!!!!")
        
        return cls.task
        

    @classmethod
    def get_satellite(cls,satcode):
        if satcode in cls.cachesats:    
            pass
        else:
            cls.cachesats[satcode] = Satellite.objects.get(noradId=satcode)

        sat = cls.cachesats[satcode]

        return sat


    #@transaction.non_atomic_requests
    #@transaction.atomic
    def post(self, request):
        try:
            serializer = TlmyRawDataSerializer(data=request.data)
                        
            if serializer.is_valid():
                                
                sat = TlmyRawDataList.get_satellite(request.data['source'])       
                
                #Funcion seleccionada por el usuario pensada para sobre-escribir la 
                #con informacion del paquete la fecha pasada al servicio
                if sat.extractDateTimeFun==None:
                    print("ExtractDatetime not available")
                    #pendiente de implementar
                    #request.data['pktdatetime'] = sat.extractdatetimefun(request.data['strdata']) 
                    
                    
                #sat = Satellite.objects.get(code=request.data['source'])
                try:
                    instance = serializer.save(satellite_id=sat.pk)
                except Exception as ex:
                    return Response(serializer.errors, status=status.HTTP_409_CONFLICT)                
                else:
                    
                    try:
                        
                        task = TlmyRawDataList.get_task()
                        #Se ha quitado Celery por el momento, solo tarea en servidor
                        task.run(TlmyRawData.objects.get(pk=instance.pk).pk, None)
                        
                    except Exception as ex:
                        print(ex.__str__())
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #TODO Se debe revisar, no envia los codigos http de respuesta correctos
        
        
        
        except IntegrityError as ex:
            data = {"error": True, "errors": ex.__str__(),}
            return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)   
            #return Response(ex, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
     
class SatelliteListView(ListAPIView):
    
    authentication_classes = [TokenAuthentication]#SessionAuthentication
    permission_classes = [IsAuthenticated]#[AllowAny]
    
    serializer_class = SatelliteSerializer
    
    def get_queryset(self):
        print(self.request.user, self.request.auth);
        return Satellite.objects.filter(active=True)
    
    
    
class TlmyVarTypeListView(ListAPIView):
    serializer_class = TlmyVarTypeSerializer
    
    #permission_classes = [DjangoModelPermissions]
    #queryset = TlmyVarType.objects.none()  # Required for DjangoModelPermissions

    
    def get_queryset(self):
        
        print("Queryset")
        satellite_id     = self.kwargs['satellite_id']
        
        if 'tlmyVarType_id' in self.kwargs:
            tlmyVarType_id   = self.kwargs['tlmyVarType_id']
            return TlmyVarType.objects.filter(satellite__id=satellite_id, id=tlmyVarType_id)
        else:    
            return TlmyVarType.objects.filter(satellite__id=satellite_id)
        
    
#ModelViewSet resuelve automaticamente esto...        
class ParameterViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication] #, 
    permission_classes = [IsAdminUser]#[AllowAny] 
    
    def get_queryset(self):
        return Parameter.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ParameterSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Parameter.objects.all()
        parameter = get_object_or_404(queryset, pk=pk)
        serializer = ParameterSerializer(parameter)
        return Response(serializer.data)   
    
    def create(self, request):
        serializer = ParameterSerializer(data=request.data)

        if serializer.is_valid():
            Parameter.objects.create(**serializer.validated_data)

            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, pk=None):
        instance = self.get_queryset().get(pk=pk)
        serializer = ParameterSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().get(pk=pk)
        serializer = ParameterSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        
        instance = Parameter.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      