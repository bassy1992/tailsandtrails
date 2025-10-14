#!/bin/bash

# Build script for Render deployment

echo "Building Tails and Trails project..."

# Backend setup
echo "Setting up Django backend..."
cd Tback
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Frontend setup
echo "Setting up React frontend..."
cd ../Tfront
npm install
npm run build:client

echo "Build completed successfully!"