DEBUG = TEMPLATE_DEBUG = False  # production
# Parse database configuration from $DATABASE_URL
import dj_database_url
import os


DATABASES = {
    'default': dj_database_url.config()
}
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
os.environ.get('DEBUG', False)

SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY', '')
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
