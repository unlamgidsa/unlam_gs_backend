'''
Created on Jul 25, 2017

@author: ubuntumate
'''

from GroundSegment.Utils.AX25 import *


if __name__ == '__main__':
    pkt = UI(b"APRS", b"FS2017", (b"WIDE1-1", b"WIDE2-1"), b"COMANDODETEST")
    