from radiocontrol.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# CELERY settings
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
BROKER_URL = 'amqp://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Vienna'

# MPD settings
MPD_SERVER = 'localhost'
MPD_PORT = 6600
