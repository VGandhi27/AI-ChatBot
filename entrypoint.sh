#!/bin/bash

# Run database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production use)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django development server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
