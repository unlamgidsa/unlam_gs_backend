'''
Created on 4 de set. de 2016

@author: Pablo Soligo
'''
from django.db import models
from GroundSegment.models.Alarm.Criticity import Criticity
from GroundSegment.models.Alarm.AlarmType import AlarmType
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.Alarm.AlarmState import AlarmState

from django.db.models.deletion import PROTECT, CASCADE



#al = Alarm.new(Satellite.objects.all()[0], AlarmType.objects.all()[0], django.utils.timezone.datetime.now(utc))

PENDING     = 0
OPEN        = 1
CLOSED      = 2

ALARM_STATUS = (
    (PENDING, 'Pendiente'),
    (OPEN, 'Abierta'),    
    (CLOSED, 'Cerrada'),
)





    
#al = Alarm.new(Satellite.objects.all()[0], AlarmType.objects.all()[0], dtArrival)
class Alarm(models.Model):
    """
    Clase/Entidad encargada de almacenar las alarmas producidas por situaciones fuera de las esperadas.
    Las alarmas pueden producirse por valores de telemetria por fuera de los rangos aceptados o situaciones no nominales    
    """
    
    alarmType = models.ForeignKey(AlarmType, related_name="alarms", on_delete=PROTECT)
    #state     = models.ForeignKey(AlarmState, related_name='alarms')
    state     = models.IntegerField() 
    dtArrival = models.DateTimeField(default=0)#(auto_now_add=True)
    satellite = models.ForeignKey('GroundSegment.Satellite', related_name='alarms', on_delete=CASCADE)
    
    
    #state     = models.ForeignKey(AlarmState, related_name='alarms')
    state     = models.IntegerField() 
    dtArrival = models.DateTimeField(auto_now_add=True)#(auto_now_add=True)
    
    
    def __init__(self, *args, **kwargs):
        super(Alarm, self).__init__(*args, **kwargs)
        
        if self.dtArrival==None:
            self.dtArrival = datetime.now(utc)
            self.state = PENDING
            
            
            
    @classmethod
    def new(cls, satellite, alarmtype, dtArrival):
        result = cls()
        result.satellite = satellite
        result.alarmType = alarmtype
        result.dtArrival = dtArrival
        result.state = PENDING
        
        #Verifico si la alarma es notificable, en caso de serlo 
        #Creo la notificacion correspondiente
        from GroundSegment.models.Notification.Notification import Notification
        result.save()
        atnts = result.alarmType.AlarmTypeNotificationTypes.all()
        for atnt in atnts:
            if atnt.notificationType.code.upper() == "EMAIL":
                #Tengo que crear una notificacion
                
                noti = Notification.new(result, atnt)
                noti.save()
                
                #Tengo que mandar email, esta claro
                
                
                
                
                

                
                                
   
 
                
            else:
                #meter if tipo case of
                pass
            
                
                
        
        return result
        
    

            
    def setOpen(self):
        """
        Este metodo verifica si es posible el cambio de estado de la alarma a abierta y en caso de ser posible lo realiza.
        Genera una excepcion en caso de no poder cumplirse la operacion
        """
        self.state = ALARM_STATUS.OPEN
        
    def setClose(self):
        """
        Este metodo verifica si es posible el cambio de estado de la alarma a cerrada y en caso de ser posible lo realiza.
        Genera una excepcion en caso de no poder cumplirse la operacion
        """
        self.state = ALARM_STATUS.CLOSED
        
        
        
    
    def isOvercome(self):
        """
        Indica si la alarma no fue antendida en el tiempo dispuesto para ello   
        """
        return (datetime.now(utc)-self.dtArrival).seconds>self.alarmType.timeout


  
    