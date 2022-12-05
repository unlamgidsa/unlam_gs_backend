'''
Created on Mar 26, 2017

@author: ubuntumate
'''
import unittest
import time

from django.utils.timezone import datetime, now, timedelta
from django.core.exceptions import ObjectDoesNotExist
import pytz
from _datetime import tzinfo
import random
from GroundSegment.models.Satellite import Satellite
#from GroundSegment.celery import loadDjangoApp
from Telemetry.models.TlmyVar import TlmyVar, TlmyVarInfo


class Test(unittest.TestCase):


    def setUp(self):
        pass
        
        
        

    def tearDown(self):
        pass



        
    def test01(self):
        sat = Satellite.objects.get(code="BDSat")
        tvt = sat.tmlyVarType.get(code="AV2868")
        tv = tvt.tlmyVars.last()
        tv.setPredictedValue("10")
        tv.save()
        self.assertEqual(tv.getPredictedValue() , 10, "No se almaceno valor predicho")
        
        pk = tv.pk
        tv = None
        tv = TlmyVar.objects.get(id=pk)
        self.assertEqual(tv.getPredictedValue() , 10, "No se almaceno valor predicho")
        
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCommand']
    unittest.main()