#!/bin/bash
set -e

echo "Starting Django application..."

# Change to the Django project directory
cd /app/Tback

# Wait a moment for any network setup
sleep 2

# Run collectstatic (safe to run multiple times)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations (safe to run multiple times)
echo "Running database migrations..."
python manage.py migrate

# Start the Django application
echo "Starting gunicorn server..."
exec gunicorn tback_api.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120