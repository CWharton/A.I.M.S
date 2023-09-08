#!/bin/bash
#
echo Running migrations for database changes.
exec python manage.py migrate
#
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn aims.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 3000