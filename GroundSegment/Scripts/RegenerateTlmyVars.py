'''
Created on 27 abr. 2020

@author: pablo
'''
import psycopg2
from GroundSegment.celery import loadDjangoApp

from django.db.models import Q

if __name__ == '__main__':
    
    loadDjangoApp()
    from GroundSegment.models.Satellite import Satellite
    from Telemetry.models.TlmyRawData import TlmyRawData
    from Telemetry.tasks import TlmyDecode
    deleteall = False;
    
    if deleteall:
        try:
            conn = psycopg2.connect("dbname='DBGS_DEVE' user='postgres' host='127.0.0.1' password='postgres'")
        except:
            print ("I am unable to connect to the database")
        #'UPDATE "GroundSegment_tlmyvartype" SET "lastCalFValue" = %s WHERE id = %s', [o.getValue(), o.pk]
        cur = conn.cursor()
        
        cur.execute("""TRUNCATE TABLE "Telemetry_tlmyvar" RESTART IDENTITY;""");
        
        cur.close()
        
    #sats = Satellite.objects.filter(active=True);
    sats = Satellite.objects.filter(~Q(code="TITA"))
    tlmydec = TlmyDecode()
    
    #PENDING PROCESED ABORTED
    for sat in sats:
        #Pasar todo a pending
        
        
        #Opcionalmente se puede procesar solo erroneos o pendientes
        #pks = sat.rawdatas.filter(Q(state=TlmyRawData.PENDING) or Q(state=TlmyRawData.ABORTED)).order_by('pktdatetime').values_list('pk', flat=True)
        
        
        pks = sat.rawdatas.order_by('pktdatetime').values_list('pk', flat=True)
        for pk in pks:
            tlmydec.run(pk, None)
            print(pk, "procesado")
    
    
    print("Fin de programa")


            
        
    
    