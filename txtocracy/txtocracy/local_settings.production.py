import os.path

import os
PATH = os.path.abspath(os.path.dirname(__file__))

def relative(path):
    return os.path.abspath(os.path.join(PATH, path))

BUCKET_NAME = "txtocracy"

DEBUG = False

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

MEDIA_ROOT = relative('media')

MEDIA_URL = "/uploads/"

STATIC_ROOT = relative('static')

STATIC_URL = 'https://txtocracy.s3.amazonaws.com/'

TEMPLATE_DIRS = (
    relative("templates")
)

DEVELOPMENT = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_QUERYSTRING_AUTH = False # Don't include auth in every url
AWS_STORAGE_BUCKET_NAME = 'txtocracy'

EMAIL_BACKEND = 'django_ses.SESBackend'
SERVER_EMAIL = 'no-reply@albertoconnor.ca'

### Analytics
GOOGLE_ANALYTICS_UA = ""
DISABLE_ANALYTICS = True

try:
    from secure_settings import *
except ImportError:
    pass