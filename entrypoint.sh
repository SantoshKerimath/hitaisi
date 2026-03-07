#!/bin/sh

echo "Starting HITAISI..."

# Only wait for postgres in docker/local
if [ "$DJANGO_ENV" = "docker" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 1
  done

  echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn core.wsgi:application --config gunicorn.conf.py