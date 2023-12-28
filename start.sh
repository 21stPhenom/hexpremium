#! /bin/sh

python manage.py migrate
gunicorn hexpremium.wsgi