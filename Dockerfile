# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    pkg-config \
    libcairo2-dev \
    netcat-openbsd \
    curl \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Cache bust: 2026-02-06-v2 (removed django-cloudinary-storage)
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create logs directory
RUN mkdir -p /app/ecommerce/logs

# Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Set working directory to where manage.py is
WORKDIR /app/ecommerce

# Expose the port the app runs on
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --forwarded-allow-ips='*' \
    ecommerce.wsgi:application
