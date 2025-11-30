#!/bin/bash

# Install backend dependencies
cd Tback
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Start Django server in background
python manage.py runserver 0.0.0.0:8000 &

# Install and build frontend
cd ../Tfront
npm install
npm run build

# Start frontend server
npm start
