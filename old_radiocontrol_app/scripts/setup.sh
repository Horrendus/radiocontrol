#!/bin/bash

export DJANGO_SETTINGS_MODULE="radiocontrol.settings.dev"
export RADIO_SECRET_KEY="dontusethiskeyinproduction"

python manage.py collectstatic --noinput

