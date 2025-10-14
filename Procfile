web: cd Tback && gunicorn tback_api.wsgi:application --bind 0.0.0.0:$PORT
release: cd Tback && python manage.py migrate