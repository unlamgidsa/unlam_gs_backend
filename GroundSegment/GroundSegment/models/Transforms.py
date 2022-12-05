'''
Created on Aug 29, 2016

@author: ubuntumate
'''

from django.db.models import Transform
from django.db import models

"""
TODO Aprender esto!
"""

class SqlLiteDatetimeDate(Transform):
    '''
    classdocs
    '''


    lookup_name = 'date'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return 'DATE({})'.format(lhs), params

    @property
    def output_field(self):
        return models.DateField()