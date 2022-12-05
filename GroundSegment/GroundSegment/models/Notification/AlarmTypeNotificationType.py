'''
Created on Sep 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Notification.NotificationType import NotificationType
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Notification.MessageTemplate import MessageTemplate
from GroundSegment.models.Notification.Contact import Contact

class AlarmTypeNotificationType(models.Model):
    """
    Clase/Entidad de configuracion donde se determina si una alarma de determinado tipo es candidata a la 
    notificacion, que tipo de notificacion de usarse, con que plantilla y cuales son los destinatarios de
    esa notificacion.
    """
    
    notificationType = models.ForeignKey(NotificationType, on_delete=models.PROTECT, related_name="AlarmTypeNotificationTypes")
    alarmType = models.ForeignKey(AlarmType, on_delete=models.PROTECT, related_name="AlarmTypeNotificationTypes")
    messageTemplate = models.ForeignKey(MessageTemplate,on_delete=models.PROTECT, related_name="AlarmTypeNotificationTypes")
    
    contacts = models.ManyToManyField(Contact, related_name="alarmTypeNotificationType")
    
    def __str__(self):
        return self.notificationType.code + "---"+self.alarmType.code + "---" + self.messageTemplate.name