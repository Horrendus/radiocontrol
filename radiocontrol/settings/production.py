from radiocontrol.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/radiocontrol.sqlite3',
    }
}

# CELERY settings
CELERY_RESULT_BACKEND = 'db+sqlite:////data/celery_results.sqlite'
BROKER_URL = 'amqp://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Vienna'

# MPD settings
MPD_SERVER = os.environ['RADIO_MPD_HOST']
MPD_PORT = os.environ['RADIO_MPD_PORT']
