'''
Created on 31 de may. de 2017

@author: pabli
'''
from GroundSegment.Utils.BColor import bcolors


NORMAL  = 1
WARNING = 2
ERROR   = 3


class Console(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    @classmethod
    def log(cls, msg, msgtype=NORMAL):

        if msgtype==NORMAL:
            msg = bcolors.OKGREEN+msg+bcolors.OKGREEN
        elif msgtype==WARNING:
            msg = bcolors.WARNING+msg+bcolors.OKGREEN
        else:
            msg = bcolors.FAIL+msg+bcolors.OKGREEN
        
        
        print(msg)
        
        