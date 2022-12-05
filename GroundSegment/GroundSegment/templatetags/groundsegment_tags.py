'''
Created on Feb 8, 2017

@author: ubuntumate
'''
from django import template
register = template.Library()

@register.filter
def mod(value, arg):
    return value % arg