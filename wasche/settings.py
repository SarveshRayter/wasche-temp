"""
Django settings for wasche project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gi68(1k7x@brmw8d+qzz^wevn90p*urqx50td-7dha_9pq=78m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost","wasche-services.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    # 'custom_user',
    # 'user.apps.UserConfig',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'application',
    'user',
    'contracts',
    'dashboard',
    'tracking_system',
    'transactions',
    "delivery_executives",
]

AUTH_USER_MODEL = "user.User"

# AUTHENTICATION_BACKENDS = ('custom_user.backends.CustomUserAuth',)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wasche.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'wasche.wsgi.application'
ASGI_APPLICATION = 'wasche.routing.application_r'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis://:IeM7xj51r6twJkXjwhGpNoOuulqvyYH4@redis-15089.c9.us-east-1-2.ec2.cloud.redislabs.com:15089/0')],
        },
    },
}
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': "wdjango",
        # 'USER':'root',
        # 'PASSWORD':'19101972',
        # 'HOST':'localhost',
        # 'PORT':'3306',
    # }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "dDI6RYQRW2",
#         'USER':'dDI6RYQRW2',
#         'PASSWORD':'YxixdpCWQH',
#         'HOST':'remotemysql.com',
#         'PORT':'3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "dbpcheriq8nqhg",
		
        'USER':'tgeqvgweqjiuea',
        'PASSWORD':'0d0a5d057517ee9efce425fc0d2ea5e2de03dd1eb07746d6fb501245d202d61f',
        'HOST':'ec2-54-197-34-207.compute-1.amazonaws.com',
        'PORT':'5432',
		
    }
}


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

USE_TZ = False

EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "wasche.services@gmail.com"
EMAIL_HOST_PASSWORD = "kpanhdgzakdemdsg"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
ENCRYPT_KEY = b'zvvhBd0Ib4Dmh4v-wfdKXH9wiW3zZG54ST4_OkmcsxA='
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]
STATIC_ROOT = os.path.join(BASE_DIR,"assets")
# STATICFILES_STORAGE = 'whitenoise.django.CompressedManifestStaticFilesStorage'
# TIME_ZONE =  'Asia/Kolkata'
# USE_I18N = True

# USE_L10N = True
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
