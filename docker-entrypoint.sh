#!/bin/bash

# Wait for database to be ready
if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
  echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
else
  echo "Skipping database wait (DB_HOST/DB_PORT not set)"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
export DJANGO_SETTINGS_MODULE=ecommerce.settings
python << END
import django
import os
from django.contrib.auth import get_user_model
django.setup()
User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'admin123'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created.')
else:
    print(f'Superuser "{username}" already exists.')
END

# Debug: Show file structure to find why statics are missing
echo "DEBUG: Current directory and files:"
pwd
ls -R | grep -v "node_modules" | head -n 30
echo "DEBUG: Contents of static folder:"
ls -R static || echo "static folder not found"

# Collect static files - DISABLED due to cloudinary_storage bug
# WhiteNoise can serve directly from STATICFILES_DIRS  
echo "Skipping collectstatic (WhiteNoise serves from STATICFILES_DIRS)..."
# python manage.py collectstatic --noinput --clear

# Start server
echo "Starting server..."
exec "$@"
