import os
from .base import *
import dj_database_url


from decouple import config
#Incorporar decouple aqui basado en la url configurada en Heroku
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rdb',
        'USER': 'ronaldomata',
        'PASSWORD': 'Afsiuvr834*',
        'HOST': '51.159.27.208',
        'PORT': '23025',
    }
}

WSGI_APPLICATION = 'datajournal.wsgi.application'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEBUG = False