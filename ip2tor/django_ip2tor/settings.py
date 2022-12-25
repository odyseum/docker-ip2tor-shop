"""
Django settings for django_ip2tor project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pprint import pprint

from environs import Env
from celery.schedules import crontab

env = Env()
env.read_env()

# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_TRANSPORT_OPTIONS = {
    # https://docs.celeryproject.org/en/stable/userguide/routing.html#redis-message-priorities
    # ['celery0', 'celery3', 'celery6', 'celery9']
    'queue_order_strategy': 'priority',
}

# CELERY_CACHE_BACKEND = 'django-cache'
# CELERY_TASK_ALWAYS_EAGER = True

CELERY_BEAT_SCHEDULE = {
    'node_alive_check': {
        'task': 'charged.lnnode.tasks.node_alive_check',
        'schedule': crontab(minute='*/30')
    }
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS=['http://localhost:8000']

# Django logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env.str('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}


INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'django_celery_results',
    'django_filters',
    'django_extensions',
    'widget_tweaks',
    'charged',
    'charged.lnnode',
    'charged.lninvoice',
    'charged.lnpurchase',
    'charged.lnrates',
    'shop.apps.ShopConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_ip2tor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Application definition
ASGI_APPLICATION = 'shop.routing.application'

WSGI_APPLICATION = 'django_ip2tor.wsgi.application'

# Use InMemoryChannelLayer in DEV only and NOT in production
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# Caching (using redis)
# https://docs.djangoproject.com/en/3.0/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Caching in Development
# https://docs.djangoproject.com/en/3.0/topics/cache/#dummy-caching-for-development

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Parse database URLs, e.g.  "postgres://localhost:5432/mydb"
DATABASES = {"default": env.dj_db_url("DATABASE_URL")}

# Parse email URLs, e.g. "smtp://"
email = env.dj_email_url("EMAIL_URL", default="smtp://")
EMAIL_HOST = email["EMAIL_HOST"]
EMAIL_PORT = email["EMAIL_PORT"]
EMAIL_HOST_PASSWORD = email["EMAIL_HOST_PASSWORD"]
EMAIL_HOST_USER = email["EMAIL_HOST_USER"]
EMAIL_USE_TLS = email["EMAIL_USE_TLS"]

SERVER_EMAIL = email.get('SERVER_EMAIL', 'root@localhost')
DEFAULT_FROM_EMAIL = email.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

ADMINS = [(env.str("DJANGO_SUPERUSER_NAME", "admin"), env.str("DJANGO_SUPERUSER_EMAIL", "root@localhost"))]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django REST Framework (DRF)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',  # is_staff must be True. ViewSet may override this.
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('de', 'German')
]

# LANGUAGES = [
#     ('en', 'English'),
# ]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# MEDIA_ROOT and MEDIA_URL are used for uploaded **non-proteced** files,
# e.g. the cover art.
# Must be separate from STATIC_ROOT and STATIC_URL
# Make sure that actually serving these file is also handled by Apache/Nginx
# and not by Django!
# https://docs.djangoproject.com/en/3.0/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

SITE_ID = 1

# further settings that can be customized (either in local_settings.py or .env)

CHARGED_LND_TLS_VERIFICATION_EDITABLE = env.bool('CHARGED_LND_TLS_VERIFICATION_EDITABLE', default=False)
CHARGED_LND_REJECT_ADMIN_MACAROON = env.bool('CHARGED_LND_REJECT_ADMIN_MACAROON', default=True)

CHARGED_COIN = env.str('CHARGED_COIN', default='BTC')
CHARGED_TAX_RATE = env.float('CHARGED_TAX_RATE', default=19)
CHARGED_TAX_CURRENCY_FIAT = env.str('CHARGED_TAX_CURRENCY_FIAT', default='EUR')
CHARGED_INFO_CURRENCIES_FIAT = env.list('CHARGED_INFO_CURRENCIES_FIAT', default=['EUR', 'USD'])

CHARGED_LNINVOICE_TIMEOUT = env.int('CHARGED_LNINVOICE_TIMEOUT', default=900)

CHARGED_LNDNODE_IMPLEMENTING_CLASSES = [ 'LndGRpcNode', 'LndRestNode']

SHOP_BRIDGE_DURATION_GRACE_TIME = env.int('SHOP_BRIDGE_DURATION_GRACE_TIME', default=600)

SHOP_OPERATOR_GROUP_NAME='operators'

WHITELISTED_SERVICE_PORTS =  env.list('WHITELISTED_SERVICE_PORTS', default=[ '8333', '9735' ])



# allow for a local file ("django_ip2tor/local_settings.py") to be used to add or override settings
if os.path.isfile(os.path.join(BASE_DIR, 'django_ip2tor', 'local_settings.py')):
    try:
        from .local_settings import *
    except ImportError:
        pass
