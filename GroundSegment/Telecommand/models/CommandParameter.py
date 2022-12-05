'''
Created on Aug 16, 2017

@author: ubuntumate
'''
from django.db import models
from .Command import Command
from django.db.models.deletion import CASCADE


class CommandParameter(models.Model):
    
    command     = models.ForeignKey(Command,related_name="parameters", on_delete=CASCADE)
    value       = models.CharField(max_length=5, default="")
    
    
    
        