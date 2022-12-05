'''
Created on 9 feb. 2021

@author: psoligo
'''

import socket
    
import ccsdspy
from ccsdspy import PacketField
import struct
       
#Conclusiones, viene la info CCDS        
        
def Nos3AdapterTCP(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = ('192.168.1.7', 7779)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    """
    pkt = ccsdspy.FixedLength([
     PacketField(name='SHCOARSE', data_type='uint', bit_length=32),
     PacketField(name='SHFINE',   data_type='uint', bit_length=20),
     PacketField(name='OPMODE',   data_type='uint', bit_length=3),
     PacketField(name='SPACER',   data_type='fill', bit_length=1),
     PacketField(name='VOLTAGE',  data_type='int',  bit_length=8),
    ])
    """
    
    ccsdspkt = ccsdspy.FixedLength([
      PacketField(name='cmdcounter', data_type='int', bit_length=8),
      PacketField(name='errocounter', data_type='int', bit_length=8),
      PacketField(name='clocks_state_flags', data_type='uint', bit_length=16),
     ])
    
    
    CFE_TIME_HKPACKET = "CFE_TIME_HKPACKET"
    
    try:
    
        # Send data
        #message = b'This is the message.  It will be repeated.'
        #print('sending {!r}'.format(message))
        #sock.sendall(message)
    
        # Look for the response
        amount_received = 0
        #amount_expected = len(message)
    
        while True:
            data = sock.recv(5000)
            amount_received += len(data)
            
            pos = data.find(CFE_TIME_HKPACKET.encode("ascii"))
            if(pos!=-1):
              
              """
              f = open('temp.bin', 'wb')
              f.write(data);
              f.close();
              result = ccsdspkt.load("temp.bin")
              print(result["clocks_state_flags"])
              """
              pkt = data[pos+len(CFE_TIME_HKPACKET):]
              
              #print("streamid", struct.unpack(">H", pkt[0:2]))
              print("Received count", struct.unpack(">I", pkt[0:4]))
              print(pkt[0:4])
              print("CCSDS_Streamid", struct.unpack(">H", pkt[4:6]))
              print("Confirmado: CCSDS_SEQUENCE", struct.unpack(">H", pkt[6:8]))
              print("CCSDS_Length", struct.unpack(">H", pkt[8:10]))
              print("CCSDS_seconds", struct.unpack("@I", pkt[10:14]))
              print("CCSDS_subsecs", struct.unpack("@H", pkt[14:16]))
              print("cmdcounter", struct.unpack("B", pkt[16:17]))
              print("errcounter", struct.unpack("B", pkt[17:18]))
              print("clockstateflags", struct.unpack("@H", pkt[18:20]))
              
              
              #print("CCSDS_subseconds", struct.unpack(">I", pkt[14:18]))
              
            
            
            
            
    
    finally:
        print('closing socket')
        sock.close()

if __name__ == '__main__':
    
    Nos3AdapterTCP(None);