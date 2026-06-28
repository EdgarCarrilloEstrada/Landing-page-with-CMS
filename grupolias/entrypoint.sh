#!/bin/sh
set -e

echo "Setting permissions..."

mkdir -p /app/static
mkdir -p /app/media

chown -R wagtail:wagtail /app/static
chown -R wagtail:wagtail /app/media

echo "Running migrations..."
python manage.py migrate --noinput

# collect all static files to the root directory
python manage.py collectstatic --no-input

# start the gunicorn worker processws at the defined port
exec gunicorn grupolias.wsgi:application --bind 0.0.0.0:8000