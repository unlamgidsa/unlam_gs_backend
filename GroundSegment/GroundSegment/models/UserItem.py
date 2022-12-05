'''
Created on 22 jul. 2020

@author: pablo
'''
from django.contrib.auth.models import User
from django.db import models
import pytz
from django.db.models.deletion import CASCADE

class UserItem(models.Model):
    jsonf = models.TextField(default="") 
    owner = models.ForeignKey(User, related_name='items' ,on_delete=CASCADE)
    