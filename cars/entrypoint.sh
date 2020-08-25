#!/bin/sh
FILE=/home/.setup_done

wait_for_db() {
  while ! nc -z $POSTGRES_DB_HOST:$POSTGRES_DB_PORT; do
    echo "waiting for $POSTGRES_DB_HOST"
    sleep 1
  done
}

setup_db() {
  wait_for_db
  python manage.py migrate
  echo "setup_db done"
  touch $FILE
}

if [ ! -f $FILE ]; then
  setup_db
fi

if [ $# -g 0 ]; then
  exec $@
else
  python manage.py collectstatic --no-input --clear
  gunicorn cars.wsgi:application --bind 0.0.0.0:$PORT
fi
