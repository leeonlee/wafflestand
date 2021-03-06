"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uqxhq$l=i4tb)4)hl9w(dgaq^0u)1p7_a9@#4-9%y+qmu+)4r4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'bluray', #the app must be before auth to override the templates
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', #for django registration
    'django.contrib.humanize', #tag library
    'south', #migrations
    'registration',
)
#need to define site_id for django.contrib.sites
SITE_ID = 1

#number of days given to activate
ACCOUNT_ACTIVATION_DAYS = 7

#email information
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_NAME", None)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PW", None)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static"),
)

# Media Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

SCRAPE_DAY = 3
RT_API_KEY = os.getenv('RT_API_KEY', None)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

isCodeship = os.getenv('PG_USER', None)
isHeroku = os.getenv('DATABASE_URL', None)

if isCodeship is not None:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': os.environ.get('PG_USER'),
            'PASSWORD': os.environ.get('PG_PASSWORD'),
            'HOST': '127.0.0.1',
        }
    }
elif isHeroku is not None:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(default='')
    DEBUG = False
