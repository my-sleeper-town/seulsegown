#!/bin/bash

/opt/venv/bin/python manage.py collectstatic

/opt/venv/bin/gunicorn seulsegown.wsgi:application --bind "0.0.0.0:8000" \
    --daemon --access-logfile - --error-logfile -

nginx -g 'daemon off;'
