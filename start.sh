#!/bin/bash

# Run Django migrations and collect static files
cd Tback

# Create migrations for any model changes
python manage.py makemigrations

# Apply migrations
# First, try to fake the problematic migration if table exists
python manage.py migrate destinations 0004_pricingtier --fake 2>/dev/null || true

# Fix pricing tier table structure if needed
python add_pricing_columns.py 2>/dev/null || true

# Then run all migrations
python manage.py migrate --run-syncdb

# Create superuser if environment variables are set
python create_superuser.py

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Start Django server on Railway's PORT
python manage.py runserver 0.0.0.0:${PORT:-8000}
