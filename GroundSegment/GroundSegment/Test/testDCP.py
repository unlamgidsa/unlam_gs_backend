'''
Created on Jan 26, 2017

@author: ubuntumate
'''
import unittest

from GroundSegment.models.DCPData import DCPData
from GroundSegment.models.DCPPlatform import DCPPlatform
from django.utils.timezone import datetime, now, timedelta, utc
import random


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDCP(self):
        for i in range(10):
            d = DCPPlatform()
            d.code = str(i)
            d.save()
         
        for d in DCPPlatform.objects.all():
            d.setData(utc, random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), random.randrange(360), random.randrange(0,10))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDCP']
    unittest.main()