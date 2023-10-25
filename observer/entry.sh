#!/bin/sh
python3 manage.py collectstatic --no-input
gunicorn observer.wsgi -b 10.123.8.17:8000 --workers=4