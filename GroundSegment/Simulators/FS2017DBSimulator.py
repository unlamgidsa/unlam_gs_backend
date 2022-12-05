'''
Created on 18 jul. 2018

@author: pablo
'''



import sys
from django.utils.datetime_safe import datetime
import time

#path = __file__

import sys, os
dire = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Utils.PktsHelpers import ExtractFS2017AX25Payload, sendJsonDataPkt

from GroundSegment.settings import APIURL

if __name__ == '__main__':
    
    import psycopg2
    from psycopg2.extras import DictCursor
    conn = psycopg2.connect("dbname=DBGS user=postgres password=postgres")
    
        
    while(True):
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("""select * from "FS2017_uhfrawdata" where upper(source)!=upper('simulation') and length(data)>80 order by created """)
            
        row = cur.fetchone()
        while row is not None:
            
            
            pktdt = datetime.utcnow()
            data = row["data"].tobytes()
            payload = ExtractFS2017AX25Payload(data)
            if payload!=None:
                sendJsonDataPkt(APIURL, pktdt, pktdt, "FS2017", row["data"].hex(), payload.hex(), False, "SIMULATION")
            print("Sleeping")
            time.sleep(5)
            row = cur.fetchone()
            
        cur.close()
    conn.close();