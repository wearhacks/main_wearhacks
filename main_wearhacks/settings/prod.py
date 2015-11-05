
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
DEBUG = os.environ.get('DEBUG', True)
TEMPLATE_DEBUG = DEBUG

#Override these using ENV Vars
SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret') 
MAPS_API_KEY = os.environ.get('MAPS_API_KEY', '')
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'mainwearhacks'
AWS_QUERYSTRING_AUTH = False

#Static root: The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = 'staticfiles'
#Static url: URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

COMPRESS_URL = STATIC_URL 

MEDIA_URL  = STATIC_URL + '/media/'
MEDIA_ROOT = os.path.join(DJANGO_ROOT, 'media_root')


COMPRESS_STORAGE = 'main_wearhacks.s3utils.CachedS3BotoStorage'
DEFAULT_FILE_STORAGE = 'main_wearhacks.s3utils.MediaRootS3BotoStorage'

COMPRESS_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
COMPRESS_OUTPUT_DIR = 'compressed'
STATICFILES_STORAGE = COMPRESS_STORAGE
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ENABLED = True
