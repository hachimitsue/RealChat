#!/bin/sh
# filepath: d:\Users\User\Desktop\CODING\RealChat\RealChat\realchat_backend\entrypoint.sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start gunicorn
echo "Starting gunicorn..."
gunicorn realchat.wsgi:application --bind 0.0.0.0:8000