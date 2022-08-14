#!/bin/sh

DJANGO_READY=/home/app/django_ready

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! /usr/bin/nc -z $SQL_HOST $SQL_PORT; do
      /bin/sleep 0.1
    done

    echo "PostgreSQL started"
fi

if ! /usr/bin/test -f "$DJANGO_READY"; then
  export DJANGO_SUPERUSER_PASSWORD="ladispe"

  # prepare Django
  /usr/local/bin/python manage.py flush --no-input
  /usr/local/bin/python manage.py migrate
  /usr/local/bin/python manage.py createsuperuser --noinput --email admin@test.org
  /usr/local/bin/python manage.py collectstatic --noinput

  # set a flag that Django is ready
  /bin/touch $DJANGO_READY

fi

exec "$@"
