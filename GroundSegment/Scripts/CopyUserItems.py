'''
Created on 22 oct. 2020

@author: pablo
'''

import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.UserItem import UserItem
from django.contrib.auth.models import User

if __name__ == '__main__':
    sa =  User.objects.get(username="sa")
    anon = User.objects.get(username="anonym")
    anon.items.all().delete()
    anon.items.add(sa.items.all()[0])
    print("Fin de programa")