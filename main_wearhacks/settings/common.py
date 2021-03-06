"""
Django settings for main_wearhacks project.
Generated by 'django-admin startproject' using Django 1.8.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from os.path import abspath, basename, dirname, normpath
import os


########## PATH CONFIGURATION

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

HTTP_PREFIX = 'http://'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/



ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (

    'events',

    'grappelli',
    'constance',

    'constance.backends.database',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
    'pipeline',
    'geoposition',
    'compressor',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'main_wearhacks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates'), os.path.join(SITE_ROOT, 'templates', 'constance')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'main_wearhacks.wsgi.application'



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
#Static root: The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(SITE_ROOT,'staticfiles')
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media_root')


# django-compressor
COMPRESS_ROOT = 'static/'
COMPRESS_URL = STATIC_URL
COMPRESS_PRECOMPILERS = (
     ('text/x-scss', 'main_wearhacks.compressor_filters.PatchedSCSSCompiler'),
)
COMPRESS_CSS_FILTERS = (
     'main_wearhacks.compressor_filters.CustomCssAbsoluteFilter',
     'compressor.filters.cssmin.CSSMinFilter'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.FileSystemFinder'
)
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'ABOUT_MISSION_STATEMENT': ('''
            <p>WearHacks is working towards building the World's Largest Hardware Lab, where the boundaries
             of imagination are explored in an intimate atmosphere, through collaboration instead of competition.</p>
            <p>Our fundamental goal is to bridge the knowledge gap that exists in the IoT industry amongst technology
             enthusiasts from all backgrounds through hackathons.</p>
            <p>We strive to make hardware education <b>accessible</b>, <b>approachable</b>,
             and <b>affordable</b>.</p>''',''),
    'ABOUT_TEAM_DESC_LEFT': ("We are a group of engineers, designers, and tinkerers that \
            all share the same vision of improving hardware education.",''),
    'AMBASSADOR_TOP_COPY': ('''<p>The WearHacks Ambassador Program offers future leaders,\
            who are truly passionate about making a change in their city, a chance to bring \
            connected technology and hardware education to their community.</p><p>\
            By building skills in <b>leadership</b>, <b>networking</b>, and <b>community\
            building</b>, WearHacks Ambassadors complete our program as experts in hacking\
            hackathons, and developing a close WearHacks community in their city.</p>'''
    ,''),
    'AMBASSADOR_BOTTOM_COPY': ('''<p class="text-center">The Ambassador Program is a volunteer \
            position, and starts 4 months before a hackathon.</p><p class="text-center">\
            A strong  successful ambassador team  comes together and begins planning their hackathon 4\
            months before the event, by taking initiatives and being self-motivated to bring the ultimate \
            WearHacks experience, and enhancing hardware education in their city's growing tech community. \
            </p>'''
    ,''),
    'PROJECTS_PAGE_TOP': ('''Each WearHacks event, with its array of projects, is a testimony to the well of talent, creativity,\
     innovative and entrepreneurial spirit that inhabits our community. Here are just a few of the submitted projects.''',''),
    'EVENTS_HACKATHON_DESC': ("<p>WearHacks Hackathons bring together developers, designers,\
            project managers, students, and engineers with an entrepreneurial and creative\
            mind.</p><p> For an intensive 48 hours, they will learn new tools, meet industry experts,\
            collaborate with other talented students and young professionals and build new\
            wearable and connected technology.</p>",''),
    'A_SOCIAL_FACEBOOK_LINK': ("http://facebook.com/wearhacks",''),
    'A_SOCIAL_YOUTUBE_LINK': ("www.google.com",''),
    'A_SOCIAL_LINKEDIN_LINK': ("https://www.youtube.com/channel/UC2ptEc6sOrLmmivfPjWoIyA",''),
    'A_SOCIAL_TWITTER_LINK': ("http://twitter.com/wearhacks",''),
    'A_BLOG_LINK':("http://blog.wearhacks.com",''),
    'CTA_EVENTS' : ('Our events provide them with unprecedented access to \
            hardware and allow their imaginations to run wild in a warm, energetic environment.',''),
    'CTA_PROJECTS' : ('Each WearHacks project is a testimony to the well of talent,\
            creativity, innovative and entrepreneurial spirit that inhabits our community.',''),
    'CTA_AMBASSADOR_PROGRAM' : ('Join our ambassador program to start the WearHacks community in your city. Apply here!', ''),
    'CTA_PARTNERSHIPS' : ('Help us create the future for the next generations of innovators.', ''),
    'LOGO_TAGLINE_SAFE' : ('Imagine Enchantment.', ''),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}