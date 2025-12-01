# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Django backend files
COPY Tback/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create staticfiles directory
RUN mkdir -p staticfiles

# Copy and make start script executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port (Railway will set PORT environment variable)
EXPOSE 8000

# Start the application
CMD ["./start.sh"]