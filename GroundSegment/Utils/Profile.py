'''
Created on 28 may. 2018

@author: pablo
'''

import cProfile

#myscript.cprof
#./env/bin/python3.5 -m cProfile -o /tmp/my-profile-data.out manage.py runserver 0.0.0.0:8000
#./env/bin/python3.5 -m cProfile -o /tmp/profile.cprof manage.py runserver 0.0.0.0:8000
#este correrlo en el directorio del virtual env
#pyprof2calltree -k -i /tmp/profile.cprof
def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func