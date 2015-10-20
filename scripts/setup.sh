#!/bin/bash

export DJANGO_SETTINGS_MODULE="radiocontrol.settings.dev"

python manage.py collectstatic --noinput

cd /
mkdir data