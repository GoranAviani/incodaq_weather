"""
Django settings for incodaq_weather project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from celery.schedules import crontab


# importing logger settings
try:
    from .logger_settings import *
except Exception as e:
    # in case of any error, pass silently.
    pass
from .local_settings import (
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
    SECRET_KEY,
    DATABASES,
    ALLOWED_HOSTS,
    GOOGLE_RECAPTCHA_SECRET_KEY
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'expanded_user.apps.ExpandedUserConfig',
    'mobile_phone.apps.MobilePhoneConfig',
    'weather.apps.WeatherConfig',
    'api_relay.apps.ApiRelayConfig',
    'django_countries',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'incodaq_weather.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'incodaq_weather.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


AUTH_USER_MODEL = 'expanded_user.custom_user'

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'



#Path settings for dev or production:
if DEBUG == True:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')





#beat settings
CELERY_BEAT_SCHEDULE = {
      'task-get_periodic_forecast_for_default_cities': {
       'task': 'weather.tasks.get_periodic_forecast_for_default_cities',
        #'schedule': crontab(minute="*/30"),
        #'schedule': 30,
        'schedule': crontab(minute=10, hour='0,2,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')
        
    },
    'task-get_forecast_for_all_users': {
        'task': 'weather.tasks.send_daily_forecast_to_all_celery',
        'schedule': crontab(minute="*/30"),
        #'schedule': 30,

    },


}



AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/auth/login/google-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'