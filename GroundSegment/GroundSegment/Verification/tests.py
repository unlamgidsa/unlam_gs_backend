'''
Created on Sep 29, 2016

@author: ubuntumate
'''
import unittest
import sys, inspect

from django.db import models
from GroundSegment.models import *

class Test(unittest.TestCase):


    def testName(self):
        """
        Prueba todos los __str__, aumenta considerablemente el code coverage
        """
        
        for name, Cls in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(Cls) and issubclass(Cls, models.Model):
                try:
                    if Cls.objects.all().count()>0:
                        obj = Cls.objects.all()[0]
                        print(obj)
                except obj.DoesNotExist:
                    pass
    
    def testSetTlmyVar(self):
        pass
        #tmt = TmlyVar
        
        #tvt = TmlyVarType.objects.
                
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()