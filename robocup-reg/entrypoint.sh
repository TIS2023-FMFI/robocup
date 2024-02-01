#!/bin/bash
export PATH=$PATH:/home/robocup/.local/bin
set -euo pipefail

pipenv run python3 manage.py migrate --force-color

if [ "${1:-prod}" = "dev" ]; then
  exec pipenv run python3 manage.py runserver 0.0.0.0:8042 --force-color
else
  pipenv run python3 manage.py collectstatic --no-input
  exec pipenv run gunicorn --bind 0.0.0.0:8042 --access-logfile - --log-file - web.wsgi
fi
