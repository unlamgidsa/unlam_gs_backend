#!/bin/bash

nginx;
uwsgi --ini /opt/app/GroundSegment/uwsgi.ini;

#/etc/init.d/nginx restart;
#/etc/init.d/nginx -g daemon off