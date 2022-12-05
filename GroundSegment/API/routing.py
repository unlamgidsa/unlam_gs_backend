'''
Created on 21 mar. 2022

@author: pabli
'''

from django.urls import re_path
from . import consumers

"""
websocket_urlptterns = [
    #re_path(r'ws/socket-server/', consumers.TlmyConsumer.as_asgi()),
    re_path(r'ws/RTTelemetry/', consumers.AsyncTlmyConsumer.as_asgi())
  ]
"""