from django.contrib import admin
from django.utils.html import mark_safe
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse

# Register your models here.
from .models.TlmyVarType import TlmyVarType, CType
from .models.TlmyVar import TlmyVar
from .models.Calibration import Calibration
from .models.Coefficient import Coefficient
from struct import unpack
from Telemetry.models.TlmyRawData import TlmyRawData
from Telemetry.tasks import TlmyDecode
from GroundSegment import settings
from django.db.models import Q
from Telemetry.AdminActions import regenerateTlmyVar, calculateOutlier,\
    forceOutlierApply, forceOutlierUnApply






class CoefficientInline(admin.TabularInline):
    model = Coefficient
    
        
class CTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'format', 'length', 'tag')
    fields = ('code', 'format', 'length', 'tag')
    
admin.site.register(CType ,CTypeAdmin)



def is_set(x, n):
    return x & 2**n != 0

class TmlyVarTypeAdmin(admin.ModelAdmin):
    #fields = ()
    search_fields = ['code']
    list_display = ('code', 'description', 'satellite', 'frameType', 'unitOfMeasurement', 'bitsLen', 'position', 'subPosition')
    fields = ('code', 'description', 'varSubType','satellite', 'subsystem','limitMaxValue', 
              'limitMinValue', 'maxValue', 'minValue', 'ctype', 'alarmType', 
              'calibrationMethod', 'frameType', 'position', 'subPosition', 'bitsLen', 
              'unitOfMeasurement', 'checkoutlier', 'outlierminlimit','outliermaxlimit' )

    list_filter = ('satellite', )
    inlines = [
        CoefficientInline,
    ]
    
    
    """
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['frameType'].queryset = FrameType.objects.filter(satellite__code='TITA')
        return super(TmlyVarTypeAdmin, self).render_change_form(request, context, *args, **kwargs)
    """
    
    
    actions = [regenerateTlmyVar, calculateOutlier, forceOutlierApply, forceOutlierUnApply]
    
            
            
    
    
admin.site.register(TlmyVarType ,TmlyVarTypeAdmin)

class TlmyVarAdmin(admin.ModelAdmin):
    list_display = ('code', 'tstamp', 'outlier')
    list_filter = ('code', 'outlier')
       

    def queryset(self, request):
        qs = super(TlmyVarAdmin, self).queryset(request)
        #qs = super(TlmyVarAdmin, self).queryset(request)
        #return qs.order_by('-id')[:100]

    """
    def queryset(self, request):
        qs = super(TlmyVarAdmin, self).queryset(request)
        return qs.order_by('-id')[:100]
    """
admin.site.register(TlmyVar ,TlmyVarAdmin)


class CalibrationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Calibration ,CalibrationAdmin)



from .models.FrameType import FrameType
class FrameTypeAdmin(admin.ModelAdmin):
    list_display = ('aid', 'description', 'satellite')
    
admin.site.register(FrameType ,FrameTypeAdmin)


from .models.UnitOfMeasurement import UnitOfMeasurement
class UnitOfMeasurementAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UnitOfMeasurement ,UnitOfMeasurementAdmin)

