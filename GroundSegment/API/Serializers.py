'''
Created on 15 may. 2018

@author: pablo
'''

from Telemetry.models.TlmyRawData import TlmyRawData
from rest_framework import routers, serializers, viewsets
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVarType import TlmyVarType, CType
from Utils.Functions import strfdelta
from django.utils.timezone import datetime, utc, now
from GroundSegment.models.Parameter import Parameter
from Telemetry.models.TlmyVar import TlmyVar
import binascii
from dateutil import tz
from GroundSegment.models.UserItem import UserItem

class THintSerializer(serializers.Serializer):
    range             = serializers.IntegerField(required=False)
    domain             = serializers.IntegerField(required=False)
    
    
    
class TlmyRawDataSerializer(serializers.Serializer):
    pktdatetime     = serializers.DateTimeField()
    


class TlmyValueSerializer(serializers.Serializer):
    key             = serializers.CharField()
    source          = serializers.CharField(required=False)
    
    name            = serializers.CharField()
    format          = serializers.CharField()
    units           = serializers.CharField(required=False)
    max             = serializers.FloatField(required=False)
    min             = serializers.FloatField(required=False)
    hints           = THintSerializer(many=False)

class TMeasuramenteSerializer(serializers.Serializer):
    key             = serializers.CharField()
    name            = serializers.CharField()
    values          = TlmyValueSerializer(many=True)
   

class TlmyDictionarySerializer(serializers.Serializer):
    
    
    key             = serializers.CharField()
    name            = serializers.CharField()
    measurements    = TMeasuramenteSerializer(many=True)
    
    
        

class ImageUrlSerializer(serializers.Serializer):
    url = serializers.URLField()
    
class TimestampField(serializers.Field):
    def to_native(self, value):
        epoch = datetime.datetime(1970,1,1)
        return int((value - epoch).total_seconds())*1000
    
#{"timestamp":1536153664159,"value":77,"id":"prop.fuel"},{"timestamp":1536153665161,"value":77,"id":"prop.fuel" max:100 min:30}
class MCTTelemetrySerializer(serializers.Serializer):
    timestamp    = serializers.IntegerField()
    value        = serializers.CharField()    
    id           = serializers.CharField()
    max          = serializers.CharField()
    min          = serializers.CharField()
    #format       = serializers.CharField()


class TlmyVarPlotSerializer(serializers.Serializer):
    xvalue  = serializers.DateTimeField()
    yvalue  = serializers.FloatField()    
    """
    Ejemplo de json
    const data = [
      {name: '1', pv: 2400},
      {name: '2', pv: 1398},
      {name: '3', pv: 9800},
      {name: '4'},
      {name: '5', pv: 4800},
      {name: '6', pv: 3800},
      {name: '7', pv: 4300},
      ];
    
    """
    

        
class TlmyVarSerializer(serializers.ModelSerializer):
    unit       = serializers.SerializerMethodField()
    
    def get_unit(self, obj):
        return obj.tlmyVarType.unitOfMeasurement.code;
    
    class Meta:
        model = TlmyVar
        fields = ('id', 'code', 'created', 'tstamp', 'calSValue', 'unit')


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite()
        fields = '__all__'
        
        
class UserItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserItem;
        fields = ["jsonf",]
        
class TlmyVarTypeSerializer(serializers.ModelSerializer):
    satellitecode       = serializers.SerializerMethodField()
    asString            = serializers.SerializerMethodField()
    updatedelta         = serializers.SerializerMethodField()
    vartype             = serializers.SerializerMethodField()
    color               = serializers.SerializerMethodField()  
    unitOfMeasurament   = serializers.SerializerMethodField()  
    

    def get_asString(self, obj):
        return obj.lastCalSValue +" "+ obj.unitOfMeasurement.code
    
    def get_satellitecode(self, obj):
        return obj.satellite.code;
    
    def get_updatedelta(self, obj):
        if obj.lastUpdate!=None:
            return strfdelta(datetime.now(utc)-obj.lastUpdate, "[{days}] {hours}:{minutes}:{seconds}")
        else:
            return "Unknown"
    
    def get_tstampdelta(self, obj):
        if obj.tstamp!=None:
            return strfdelta(datetime.now(utc)-obj.tstamp, "[{days}] {hours}:{minutes}:{seconds}")
        else:
            return "Unknown"
    def get_vartype(self, obj):
        return CType.VARTYPE[obj.varType][1]
    
    def get_unitOfMeasurament(self, obj):
        return obj.unitOfMeasurement.code
    
    def get_color(self, obj):
        if obj.ctype.varType in [0, 1]: #float intenger
            
            
            units = obj.limitMaxValue-obj.limitMinValue
            blockerror = units*0.15
            blockwarning = units*0.25
            value = obj.getValue()
            if (value<obj.limitMinValue+blockerror) or (value>obj.limitMaxValue-blockerror):
                color = 'red'
            elif (value<obj.limitMinValue+blockwarning) or (value>obj.limitMaxValue-blockwarning): 
                color = 'yellow'
            else:   
                color = 'green'
        
            return color;
        else:   
            return 'green'
    #def get_subsustem(self, obj):
    #    return obj.subsystem.code
    
    class Meta:
        model  = TlmyVarType;
        fields = ['id', 'satellitecode','code', 'description', 'lastCalSValue', 
                  'asString', 'lastUpdate', 'tstamp', 'updatedelta', 'tstamp', 
                  'vartype', 'limitMaxValue', 'limitMinValue', 'color', 
                  'unitOfMeasurament']
        


# Serializers define the API representation.
class TlmyRawDataSerializer(serializers.Serializer):
    capturedAt  = serializers.DateTimeField(required=True)
    pktdatetime = serializers.DateTimeField(required=True)
    source      = serializers.CharField(default='simulation')
    strdata     = serializers.CharField(default='')
    realTime    = serializers.BooleanField(default=False)
    tag         = serializers.CharField(max_length=24, default='TEST')
        
    #pylStart    = serializers.IntegerField(default=0)
    #pylEnd      = serializers.IntegerField(default=0)
    
    def create(self, validated_data):
        """
        Create and return a new `TlmyRawData` instance, given the validated data.
        """
        nd = TlmyRawData()
        nd.capturedAt       = validated_data['capturedAt']
        nd.pktdatetime      = validated_data['pktdatetime']
        
        nd.source           = validated_data['source']
        
        #TODO delete
        #nd.strdata          = validated_data['strdata']
        
        nd.realTime         = validated_data['realTime']  
        nd.tag              = validated_data['tag']
        nd.satellite_id     = validated_data['satellite_id']
        nd.data             = binascii.unhexlify(validated_data['strdata'])       
        nd.save()
        
        
        return nd

    
    
    #TlmyRawData
    #
    #    fields = ('capturedAt', 'pktdatetime', 'source', 'strdata', 'realTime', 'tag', 'strpayload')
        
        
class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
     
        
        
