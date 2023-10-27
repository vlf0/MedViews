#!/bin/sh
python3 manage.py collectstatic --noinput
gunicorn observer.wsgi -b 0.0.0.0:8000 --workers=4
