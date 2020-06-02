#!/usr/bin/env bash

# start background tasks
python manage.py process_tasks &
gunicorn --workers=12 -b :$PORT djangowebscraperapp.wsgi