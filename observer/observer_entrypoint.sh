#!/bin/sh
python3 manage.py collectstatic --no-input
gunicorn observer.wsgi -b 0.0.0.0:8000