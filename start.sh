#!/bin/bash

# Run Django migrations and collect static files
cd Tback
python manage.py migrate
python manage.py collectstatic --noinput

# Start Django server in background on port 8000
python manage.py runserver 0.0.0.0:8000 &

# Start frontend server on PORT (Railway will set this)
cd ../Tfront
PORT=${PORT:-3000} node dist/server/node-build.mjs
