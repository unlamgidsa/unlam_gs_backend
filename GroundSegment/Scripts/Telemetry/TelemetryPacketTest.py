'''
Created on 02-nov-2020

@author: pabli
'''
import os, sys, time
import binascii
import struct
import datetime

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj_path = 'C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


from GroundSegment.models.Satellite import Satellite

if __name__ == '__main__':
    #Lituanicasat 2 telemetry analysis
    #cad = "86A2404040400098B26098A6400103F00AAA0000700007020008FDFF03000008FDFF0400170000001700000000000000F1A900000000EC06808C809E44100000000027002700760B3D06FCA900007000150F005C26255C0800007054000400B9006800FA00010A0029007F0100010101010000000000000000000000005200000040420F0000000000000000000000000000000000000000000000000000000000000000000000000041014C015301DC1F00002C0000000900930000000000000049006400010018000000000000000000000000925201003709000007000800070008000000000001030106000000000000000001"
    #pkt = binascii.unhexlify(cad)
        
    
    lit = Satellite.objects.get(code="Lituanicasat-2")
    raws = lit.rawdatas.all()
    offset = 0
    basedate = datetime.datetime(1970,1,1)
    ADCSTimePos = 104
    
    for raw in raws:
        pkt = raw.getPayloadBlob()
        print(pkt.hex())
        if(len(pkt)>200):
            buff = pkt[ADCSTimePos-offset:ADCSTimePos-offset+4]
            delta = datetime.timedelta(seconds=struct.unpack("<I", buff)[0])
            print("dt=", basedate+delta)
            
          
    
    
    
    