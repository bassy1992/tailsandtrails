#!/bin/bash

# Run Django migrations and collect static files
cd Tback

# Create migrations for any model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Start Django server on Railway's PORT
python manage.py runserver 0.0.0.0:${PORT:-8000}
