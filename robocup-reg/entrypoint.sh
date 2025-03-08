#!/bin/bash
set -euo pipefail


if [ "${1:-prod}" = "docker" ]; then
  python manage.py migrate --force-color
  python manage.py collectstatic --no-input
  exec gunicorn --bind 0.0.0.0:8000 --access-logfile - --log-file - web.wsgi
else
  export PATH=$PATH:/home/robocup/.local/bin
  pipenv run python3 manage.py migrate --force-color
  pipenv run python3 manage.py collectstatic --no-input
  exec pipenv run gunicorn --bind 0.0.0.0:8042 --access-logfile - --log-file - web.wsgi
fi
