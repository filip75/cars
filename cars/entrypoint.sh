#!/bin/sh
FILE=/code/.setup_done

wait_for_db() {
  while ! nc -z $POSTGRES_DB_HOST:$POSTGRES_DB_PORT; do
    echo "waiting for $POSTGRES_DB_HOST"
    sleep 1
  done
}

setup_db() {
  wait_for_db
  python /code/manage.py migrate
  echo "setup_db done"
  touch $FILE
}

if [ ! -f $FILE ]; then
  setup_db
fi

python /code/manage.py runserver 0.0.0.0:$PORT
