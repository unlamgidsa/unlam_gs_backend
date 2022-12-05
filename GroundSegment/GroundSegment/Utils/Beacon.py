'''
Created on Jul 25, 2017

@author: ubuntumate
'''
#!/Beacon.py

# Quick and dirty APRS beacon generator
# By Erik Brom, WB0NIU, 9/10/2015
#
# You can connect this to any TNC's KISS port, as long as it available via network
#
# Thanks to:
#   Mitch, AB4MW
#   John, WB2OSZ
#
# References:
#   https://github.com/wb2osz/direwolf
#   https://www.tapr.org/pub_ax25.html#2.3.5.4
#   http://www.ka9q.net/papers/kiss.html
#   Direwolf ax25_pad.c

# This is my first significant Python program, so forgive me if it is poor format!
# A couple questions:
#   Should the MSB of the control byte for the destination address be set?
#   Where does the CRC get added.  It's not done by this program but it does work.

import socket


# Simple test function to dump a string in both ASCII and Hex
# For testing what I'm generating:
def dumpstring(str):
    for x in range(0,len(str)):
        print( str[x] ),
        print (' {0:X}'.format(ord(str[x])))



# From Direwolf ax25_pad.c:
# *    Each address is composed of:
# *
# *    * 6 upper case letters or digits, blank padded.
# *        These are shifted left one bit, leaving the the LSB always 0.
# *    * a 7th octet containing the SSID and flags.
# *        The LSB is always 0 except for the last octet of the address field.
# This function formats the first 6 characters
def format_call(raw_call):
    raw_call = raw_call.upper()
    while len(raw_call) < 6:
        raw_call = raw_call + chr(0x20)

    result = ''
    for x in range(0,6):
        result = result + chr( ord(raw_call[x]) << 1)
    return result


# From Direwolf ax25_pad.c:
# *
# *    A UI frame starts with 2-10 addressses (14-70 octets):
# *
# *    * Destination Address
# *    * Source Address
# *    * 0-8 Digipeater Addresses  (Could there ever be more as a result of 
# *                    digipeaters inserting their own call
# *                    and decrementing the remaining count in
# *                    WIDEn-n, TRACEn-n, etc.?   
# *                    NO.  The limit is 8 when transmitting AX.25 over the radio.
# *                    However, communication with an IGate server could have 
# *                    a longer VIA path but that is only in text form, not here.)
# *
# *    Each address is composed of:
# *
# *    * 6 upper case letters or digits, blank padded.
# *        These are shifted left one bit, leaving the the LSB always 0.
# *    * a 7th octet containing the SSID and flags.
# *        The LSB is always 0 except for the last octet of the address field.
# *
# *    The final octet of the Destination has the form:
# *
# *        C R R SSID 0, where,
# *
# *            C = command/response = 1
# *            R R = Reserved = 1 1
# *            SSID = substation ID
# *            0 = zero
# *
# *    The final octet of the Source has the form:
# *
# *        C R R SSID 0, where,
# *
# *            C = command/response = 1
# *            R R = Reserved = 1 1
# *            SSID = substation ID
# *            0 = zero (or 1 if no repeaters)
# *
# *    The final octet of each repeater has the form:
# *
# *        H R R SSID 0, where,
# *
# *            H = has-been-repeated = 0 initially.  
# *                Set to 1 after this address has been used.
# *            R R = Reserved = 1 1
# *            SSID = substation ID
# *            0 = zero (or 1 if last repeater in list)
# *
# *        A digipeater would repeat this frame if it finds its address
# *        with the "H" bit set to 0 and all earlier repeater addresses
# *        have the "H" bit set to 1.  
# *        The "H" bit would be set to 1 in the repeated frame.
# *
# *    When monitoring, an asterisk is displayed after the last digipeater with 
# *    the "H" bit set.  No asterisk means the source is being heard directly.
# *
# *    Example, if we can hear all stations involved,
# *
# *        SRC>DST,RPT1,RPT2,RPT3:        -- we heard SRC
# *        SRC>DST,RPT1*,RPT2,RPT3:    -- we heard RPT1
# *        SRC>DST,RPT1,RPT2*,RPT3:    -- we heard RPT2
# *        SRC>DST,RPT1,RPT2,RPT3*:    -- we heard RPT3
# *
# *    
# *    Next we have:
# *
# *    * One byte Control Field     - APRS uses 3 for UI frame
# *                       The more general AX.25 frame can have two.
# *
# *    * One byte Protocol ID         - APRS uses 0xf0 for no layer 3
# *
# *    Finally the Information Field of 1-256 bytes.
# *
# *    And, of course, the 2 byte CRC.

def buildUIFrame(dest_call, source_call, text):
    # ax.25 UI frame has 7 chars for dest, 7 chars for source, one byte 
    # for frame type of UI (03), and one byte for protocol ID (f0)
    # See ax25_pad.c for packet format


    path1 = "WIDE1" # Hard coded path.  SSID is part of the flag byte below
    path2 = "WIDE2" # TODO: Pass this in and parse it.
    result = format_call(dest_call)
    result = result + chr(0xe0)                  # SSID = 0
    result = result + format_call(source_call)
    result = result + chr(0xfe) # -15            # SSID = 15.  Should the MSB be set? Seems to work either way
    result = result + format_call(path1)
    result = result + chr(0x62)                  # 0 1 1 0001 0: WIDE1-1  
    result = result + format_call(path2)
    result = result + chr(0x65)                  # 0 1 1 0010 1: WIDE2-2, last address
    result = result + chr(0x03) + chr(0xf0)
    result = result + text

    return result


# Wrap the formatted packet in a KISS wrapper to send to the TNC

KISS_ID = 0x00
FEND = 0xC0
FESC = 0xDB
TFEND = 0xDC
TFESC = 0xDD;

def KissWrap(packet):
    # John Langner's way from C in Direwolf 1.2
    # Wrap it in C0 00 <packet> C0, and escape any data of that value
    result = chr(FEND) + chr(KISS_ID)
    for i in range(0,len(packet)):
        if (packet[i] == chr(FEND)):
            result = result + chr(FESC) + chr(TFEND)
        elif (packet[i] == chr(FESC)):
            result = result + chr(FESC) + chr(TFESC)
        else:
            result = result + packet[i]

    result = result + chr(FEND)
    return result



# Mainline of the program:

#----server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#Fill in the name and port number of the server with the KISS TNC.
#----host = socket.gethostbyname('192.168.1.97')
#----port = 6700
#----MYCALL = "mycall"

#----server.connect((host,port))


#----frame = buildUIFrame("Python",MYCALL,">test of my Python script.")

#----frame = KissWrap(frame)
#----print "the kiss frame is:",len(frame)
#----dumpstring(frame)

#and send it
#----server.send(frame)

