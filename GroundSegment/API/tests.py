from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
import json
from Scripts.DataCreation import DataCreation


class Test(APITestCase):


    def setUp(self):
        pass
        
                

    def tearDown(self):
        pass
    
    @classmethod
    def setUpClass(cls):
        """
        Crea los maestros de operacion para el resto de los test de esta unidad
        """
        super(Test, cls).setUpClass()
        print("Creando datos maestros...")
        DataCreation()
        print("Datos maestros creados.")
        pass
    
    #@classmethod
    #def setUpTestData(cls):
    #    call_command('loaddata', 'myfile', verbosity=0)
        
    
    def testAddTelemetryRawPkt(self):
        """
        Ensure we can create a new account object.
        """
        dt = datetime.utcnow()
        
        for i in range(0,9999):
            jdata = {}
            jdata['capturedAt']     = dt.isoformat()
            jdata['pktdatetime']    = dt.isoformat()
            jdata['source']         = "LITUANICASAT2"
            jdata['strdata']        = "86A2404040400098B26098A6400103F064E900007000FE020008F5FF03000008F7FF040027000000270000000000000031E900000000EB0680A0808C4E1600000700320032007F0B46063DE9000070000D08008A95F45A0400008055FFFFFF47013FFEFF0101A6003E00DE020001010101000000000000000000000000B300000040420F000000000000000000000000000000000000000000000000000000000000000000000000001E13E31253014020C201670000002D01930000000000000049005B00010018000000000000000000000000DAF901009108000001000100000001000000000001030106000000000000000001"
            jdata['realTime']       = False
            jdata['tag']            = "FALSEDATA"
            jsondata                = json.dumps(jdata)
            
            url = reverse('TlmyRawData-APIPost')
            
            response = self.client.post(url, jsondata, content_type='application/json')
            dt = datetime.utcnow()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
        
        