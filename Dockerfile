# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install pnpm
RUN npm install -g pnpm

# Copy backend requirements and install Python dependencies
COPY Tback/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend package files and install dependencies
COPY Tfront/package.json Tfront/pnpm-lock.yaml /app/Tfront/
WORKDIR /app/Tfront
RUN pnpm install

# Copy all source code
WORKDIR /app
COPY . /app/

# Build frontend
WORKDIR /app/Tfront
RUN pnpm run build

# Collect Django static files
WORKDIR /app/Tback
RUN python manage.py collectstatic --noinput

# Create staticfiles directory
RUN mkdir -p /app/Tback/staticfiles

# Copy and make start script executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Set working directory back to app root
WORKDIR /app

# Expose port
EXPOSE $PORT

# Start the application
CMD ["bash", "start.sh"]