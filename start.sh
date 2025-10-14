#!/bin/bash

echo "Starting Django application..."

# Change to the Django project directory
cd /app/Tback

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Start gunicorn server
echo "Starting gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 tback_api.wsgi:application