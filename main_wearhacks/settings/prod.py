DEBUG = TEMPLATE_DEBUG = False  # production
# Parse database configuration from $DATABASE_URL
import dj_database_url
import os
from .common import SITE_NAME, DJANGO_ROOT, SITE_ROOT

DATABASES = {
    'default': dj_database_url.config()
}
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
DEBUG= os.environ.get('DEBUG', True)

SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY', '')
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'mainwearhacks'

STATIC_ROOT = 'staticfiles'
STATIC_URL = 'http://mainwearhacks.s3.amazonaws.com/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)
COMPRESS_URL = STATIC_URL
#Put private variables here (or env)
COMPRESS_ENABLED = True


COMPRESS_STORAGE = 'main_wearhacks.s3utils.CachedS3BotoStorage'

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

COMPRESS_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/javascript')
COMPRESS_OUTPUT_DIR = 'compressed'
STATICFILES_STORAGE = COMPRESS_STORAGE

COMPRESS_URL = STATIC_URL
COMPRESS_ENABLED = True
