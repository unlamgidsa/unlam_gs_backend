#!/bin/bash
cd /home/pablo/git/GroundSegment/GroundSegment
source /home/pablo/.local/share/virtualenvs/GroundSegment-P2spt5oE/bin/activate
uwsgi --http :8000 --processes 4 --threads 2 --chdir ./ --wsgi-file wsgi.py &
celery -A GroundSegment  worker -c=1 -l info &
celery -A GroundSegment beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & 
celery -A GroundSegment flower --port=23355

