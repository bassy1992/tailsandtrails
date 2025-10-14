#!/bin/bash
set -e

echo "Starting Django application..."

cd /app/Tback

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate

echo "Starting gunicorn server..."
exec gunicorn tback_api.wsgi:application --bind 0.0.0.0:$PORT