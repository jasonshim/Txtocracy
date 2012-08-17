
import os.path

import os
PATH = os.path.abspath(os.path.dirname(__file__))

def relative(path):
    return os.path.abspath(os.path.join(PATH, path))

DEBUG = True

MEDIA_ROOT = relative('media')

MEDIA_URL = "/uploads/"

STATIC_ROOT = relative('static')

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    relative("templates")
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': relative('data.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DEVELOPMENT = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'