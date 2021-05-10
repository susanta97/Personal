"""
Django settings for Personal project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gv&e0rto@iz&t#2v=*zhm$y$07^!=ok-s%dl5hvllouy==)p65'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
    'account.apps.AccountConfig',
    'usrprofile.apps.UsrprofileConfig',
    'crispy_forms',


]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Personal.urls'

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

WSGI_APPLICATION = 'Personal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'My_Personal1',
    }
}

# CACHES = {
#     'default': {
#     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#     'LOCATION': '127.0.0.1:11211',
#     'TIMEOUT': 60
# }
# }



CACHE_TTL = 60 * 0.5
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MASTER_CACHE': '192.168.0.112:6379',
            # 'PASSWORD' : 'mypassword'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
#
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATIC_ROOT = os.path.join(BASE_DIR ,'staticcdn')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shreyadatta420@gmail.com'
EMAIL_HOST_PASSWORD = 'Riju8100006942'



AUTH_USER_MODEL='account.Account'


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS=[
    os.path.join(BASE_DIR , 'static'),
    os.path.join(BASE_DIR, 'media')
]
STATIC_ROOT=os.path.join(BASE_DIR , 'static_cdn')
MEDIA_ROOT=os.path.join(BASE_DIR , 'media_cdn')

TEMP=os.path.join(BASE_DIR , 'media_cdn/temp')

BASE_URL='127.0.0.1:8000'



# MEDIA_URL='/media/'
# MEDIA_ROOT=[
#     os.path.join(BASE_DIR , 'media')
#
# ]

# STATIC_DIR=[
#     os.path.join(BASE_DIR , 'static'),
#     # os.path.join(BASE_DIR , 'medis')
# ]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

RUN_PRODECTION_SERVER=False
RUN_DEVELOPEMENT_SERVER=True

LOGIN_URL='accounts:login'
LOGIN_REDIRECT_URL = 'home:home'