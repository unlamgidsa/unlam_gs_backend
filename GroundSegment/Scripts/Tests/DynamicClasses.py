'''
Created on 3 abr. 2020

@author: pablo
'''
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.celery import loadDjangoApp

loadDjangoApp();

from django.db import models
from Telemetry.models.TlmyVar import TlmyVar



def create_model(name, fields=None, app_label='', module='', options=None, tbl=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        db_table = tbl
        

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options:
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)
    # model.db_table = tbl
    # Create an Admin class if admin options were provided
    
    return model
    

if __name__ == '__main__':
    
    tables = ["Telemetry_tlmyvar", "Telemetry_htlmyvar"]
        
    table_map = {}
    for tbl in tables:
        
        fields = {'code' : models.CharField(max_length=24)}
        options = {}
        #                            (name, fields=None, app_label='', module='', options=None, tbl=None):
        table_map[tbl] = create_model(tbl, fields, app_label="Dynamic", module="Dynamic", options=options, tbl=tbl)
        
    
    
    print("->",table_map["Telemetry_htlmyvar"].objects.first().code)        
            
        
        

