#!/bin/bash

#Upgrade the database
python manage.py migrate || exit 1

echo "$DJANGO_SETTINGS_MODULE"

celery -A radiocontrol worker -l info &

#Run the application
uwsgi \
	--static-map /static=static \
	--static-map /public=public \
	--https 0.0.0.0:443,/data/certs/radiocontrol.crt,/data/certs/radiocontrol.key \
	--file radiocontrol/wsgi.py \