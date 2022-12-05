'''
Created on 30 de ago. de 2016

@author: pabli
'''

from datetime import datetime


"""
Usada por pyephem
"""

def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime(year, month, day, hour, minute, int(second))
    return dt

def get_next_pass(lon, lat, alt, tle):

    import ephem
    
    sat = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(lon)
    observer.elevation = alt
    observer.pressure = 0
    observer.horizon = '-0:34'

    now = datetime.utcnow()
    observer.date = now

    tr, azr, tt, altt, ts, azs = observer.next_pass(sat)

    duration = int((ts - tr) *60*60*24)
    rise_time = datetime_from_time(tr)
    max_time = datetime_from_time(tt)
    set_time = datetime_from_time(ts)

    observer.date = max_time

    sun = ephem.Sun()
    sun.compute(observer)
    sat.compute(observer)

    sun_alt = degrees(sun.alt)

    visible = False
    if sat.eclipsed is False and -18 < degrees(sun_alt) < -6 :
        visible = True

    return {
             "rise_time": timegm(rise_time.timetuple()),
             "rise_azimuth": degrees(azr),
             "max_time": timegm(max_time.timetuple()),
             "max_alt": degrees(altt),
             "set_time": timegm(set_time.timetuple()),
             "set_azimuth": degrees(azs),
             "elevation": sat.elevation,
             "sun_alt": sun_alt,
             "duration": duration,
             "visible": visible
           }