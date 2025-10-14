# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY Tback/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create staticfiles directory
RUN mkdir -p /app/Tback/staticfiles

# Expose port
EXPOSE 8000

# Change to Tback directory and start the application
WORKDIR /app/Tback
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn tback_api.wsgi:application --bind 0.0.0.0:$PORT"]