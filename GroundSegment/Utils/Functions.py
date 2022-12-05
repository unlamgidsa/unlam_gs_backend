'''
Created on 11 jul. 2018

@author: pablo
'''
import time



def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def dtToUnixTime(dt):
    return time.mktime(dt.timetuple())