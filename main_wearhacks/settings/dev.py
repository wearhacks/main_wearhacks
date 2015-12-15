from .common import SITE_NAME, DJANGO_ROOT, SITE_ROOT
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DJANGO_ROOT, 'db.sqlite3'),
    }
}
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY', '')
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'mainwearhacks'
AWS_QUERYSTRING_AUTH = False
#COMPRESS_ENABLED = True
STRIPE_SECRET_KEY = os.environ.get('TEST_STRIPE_SECRET_KEY',
    '')
STRIPE_PUBLIC_KEY = os.environ.get('TEST_STRIPE_PUBLIC_KEY',
    '')


COLLECTFAST_ENABLED = False
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static'),
  )
