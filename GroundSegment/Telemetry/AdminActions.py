'''
Created on 27-oct-2020

@author: pabli
'''
from Telemetry.tasks import TlmyDecode
'''
Created on 26-oct-2020

@author: pabli
'''
from django.contrib import admin
import numpy as np
from django.core.wsgi import get_wsgi_application
from django.db.models import Q
from GroundSegment.models.Satellite import Satellite
from Telemetry.models.TlmyVar import TlmyVar


def forceOutlierUnApply(modeladmin, request, queryset):
    for tlt in queryset:
        vars = tlt.tlmyVars.all()
        for var in vars:
            var.outlier = False
            #var.save()
        
        TlmyVar.objects.bulk_update(vars, ['outlier'])
        
forceOutlierUnApply.short_description =  "Force Not apply outlier"




def forceOutlierApply(modeladmin, request, queryset):
    for tlt in queryset:
        vars = tlt.tlmyVars.all()
        for var in vars:
            if tlt.checkoutlier==True:
                if var.rawValue>tlt.outliermaxlimit or var.rawValue<tlt.outlierminlimit:
                    var.outlier = True
                    #print("Var de tipo", tlt.code, "tiene outlier aplicado")
                else:
                    var.outlier = False
            else:
                var.outlier = False;    
            #var.save()
        
        print("Actualizando: ", tlt.code)
        TlmyVar.objects.bulk_update(vars, ['outlier'])
        print(tlt.code, "actualizado")
        
forceOutlierApply.short_description =  "Force apply outlier"

    
def calculateOutlier(modeladmin, request, queryset):
    for tlt in queryset:
        print("Procesando: ", tlt.code)
        
        lastval = tlt.tlmyVars.filter(~Q(rawValue=0.0))[:1000].values_list('rawValue', flat=True)
        if(len(lastval)>0):
            Q1 = np.percentile(lastval, 25, interpolation = 'midpoint')  
            Q2 = np.percentile(lastval, 50, interpolation = 'midpoint')  
            Q3 = np.percentile(lastval, 75, interpolation = 'midpoint')  
            IQR = Q3 - Q1  
            print('Interquartile range is', IQR) 
            low_lim = Q1 - 1.5 * IQR 
            up_lim = Q3 + 1.5 * IQR 
            print('low_limit is', low_lim) 
            print('up_limit is', up_lim) 
            #Si los limites son distintos darle gas
            if low_lim!=up_lim:
                print("Tipo ", tlt.code, "se le aplican outlier, limites", low_lim, up_lim)
                tlt.checkoutlier = True
                tlt.outliermaxlimit = up_lim;
                tlt.outlierminlimit = low_lim;
                
            else:
                print("Tipo ", tlt.code, "limites no aplicables", low_lim, up_lim)
                tlt.checkoutlier = False
                tlt.outliermaxlimit = 0;
                tlt.outlierminlimit = 0;
                
            tlt.save()            
        else:
            tlt.checkoutlier = False
            tlt.outliermaxlimit = 0;
            tlt.outlierminlimit = 0;
            tlt.save()


calculateOutlier.short_description =  "Calculate outlier limits"
            
            
def regenerateTlmyVar(modeladmin, request, queryset):
    #borro la historia
    
    task = TlmyDecode()
    print("Borrado de variables")
    for tvt in queryset:
        vars = tvt.tlmyVars.all()[:1000]
        #qs = tvt.tlmyVars.all()
        #qs._raw_delete(qs.db)
        while vars.count()>0:
            for var in vars:
                var.delete()
            vars = tvt.tlmyVars.all()[:1000]
            print("1000", tvt.code, "borradas")
        #tvt.tlmyVars.all()[:1000].delete()
        
    print("Variables eliminadas, se inicia regeneracion")
        
    
    pks = queryset.first().satellite.rawdatas.values_list("pk", flat=True)
    
    print("Raws obtenidos, se inicia proceso...")
    for pk in pks:
        task.run(pk, queryset)
        
    return request

  
        
regenerateTlmyVar.short_description =  "Generar/Regenerar la variable"
