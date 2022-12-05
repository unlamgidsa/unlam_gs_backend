'''
Created on 16 de ago. de 2016
@author: pabli
'''

from django.utils.html import mark_safe
from django.db import models
from django.contrib import admin
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Tle import Tle
from GroundSegment.models.Parameter import Parameter

from GroundSegment.models.SatelliteState import SatelliteState
#from GroundSegment.models.Pasada import Pass
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models.Alarm.Criticity import Criticity
from GroundSegment.models.Alarm.AlarmState import AlarmState
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.Sitio import Sitio

from GroundSegment.models.Notification.AlarmTypeNotificationType import AlarmTypeNotificationType
from GroundSegment.models.Notification.Contact import Contact
from GroundSegment.models.Notification.MessageTemplate import MessageTemplate
from GroundSegment.models.Notification.Notification import Notification
from GroundSegment.models.Notification.NotificationType import NotificationType



from GroundSegment.models.SubSystem import SubSystem
from GroundSegment.models.Log import Log



from GroundSegment.models.DCPPlatform import DCPPlatform
from GroundSegment.models.DCPData import DCPData
from GroundSegment.models.Country import Country
from GroundSegment.models.State import State

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from GroundSegment.models.Eclipse import Eclipse
from GroundSegment.models.UserItem import UserItem

from rest_framework.authtoken.admin import TokenAdmin
from django.forms.widgets import Textarea


TokenAdmin.raw_id_fields = ['user']

class SatelliteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Satellite, SatelliteAdmin)


class ParameterAdmin(admin.ModelAdmin):
    search_fields = ['module']
    list_display = ('module', 'key', 'value', 'description')

admin.site.register(Parameter, ParameterAdmin)



class SatelliteStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(SatelliteState, SatelliteStateAdmin)


class AlarmTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AlarmType, AlarmTypeAdmin)

class UserItemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 512,
                                  'cols': 40,
                                  'style': 'height: 1em;'})},
    }

admin.site.register(UserItem, UserItemAdmin)

class AlarmAdmin(admin.ModelAdmin):
    pass

admin.site.register(Alarm, AlarmAdmin)


class CriticityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Criticity, CriticityAdmin)

class AlarmStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(AlarmState, AlarmStateAdmin)


class PasadaAdmin(admin.ModelAdmin):
    list_display = ('satellite', 'sitio', 'startTime', 'stopTime', 'getDurationStr')
    list_filter = ['satellite', 'sitio', 'startTime']

admin.site.register(Pasada,PasadaAdmin)


class EclipseAdmin(admin.ModelAdmin):
    list_display = ('satellite', 'startTime', 'stopTime', 'getDurationStr')
    list_filter = ['satellite', 'startTime']

admin.site.register(Eclipse,EclipseAdmin)


class SitioAdmin(admin.ModelAdmin):
    pass

    def clean(self):
        # Validation goes here :)
        raise forms.ValidationError("MAL!!!")

admin.site.register(Sitio,SitioAdmin)

class ContactAdmin(admin.ModelAdmin):
    fields = ('name', 'email',)
    list_display = ('name', 'email',)
admin.site.register(Contact ,ContactAdmin)

class AlarmTypeNotificationTypeAdmin(admin.ModelAdmin):
    
    fields = ('notificationType', 'alarmType', 'messageTemplate', 'contacts',)
    list_display = ('notificationType', 'alarmType', 'messageTemplate',)
admin.site.register(AlarmTypeNotificationType ,AlarmTypeNotificationTypeAdmin)



class MessageTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(MessageTemplate ,MessageTemplateAdmin)

class NotificationTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(NotificationType ,NotificationTypeAdmin)

class NotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notification ,NotificationAdmin)









class SubSystemAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubSystem ,SubSystemAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'module', 'logType')
    search_fields = ['module', 'logType']
    list_filter = ['module', 'logType']

    def get_queryset(self, request):
    #def queryset(self, request):
        qs = super(LogAdmin, self).get_queryset(request)
        tmp = qs.all().order_by("-id")
        return tmp
    
admin.site.register(Log ,LogAdmin)

class DCPPlatformAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(DCPPlatform ,DCPPlatformAdmin)

class DCPDataAdmin(admin.ModelAdmin):
    list_display = ('dcp_plataform', 'dataTime', 'Precipitation','Humidity')
#    readonly_fields=('dcp_plataform', 'dataTime', 'Precipitation','Humidity')
admin.site.register(DCPData ,DCPDataAdmin)


class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Country, CountryAdmin)

class StateAdmin(admin.ModelAdmin):
    pass

admin.site.register(State, StateAdmin)

