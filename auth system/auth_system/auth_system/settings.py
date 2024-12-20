"""
Django settings for auth_system project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zrjd%#x)@j5ceu*%017^%f@z!y(^uv0efw1@vnpx%x%^8@$7nl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# WORKING_HOURS_START 
WORKING_HOURS_START = '08:00'
MINIMUM_LEAVE_DAYS_WARNING = 3

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # new app
    'main',
    'channels',
    'users',
    'business_logic',
    'dashboard_admin',
    'rest_framework',
    'django.contrib.sites',
    'tinymce',
    'captcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'fontawesomefree',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_extensions',
]
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

GRAPH_MODELS = {
  'app_labels': ["users", "main"],
}

SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET=True

AUTH_USER_MODEL = 'users.CustomUser'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

ASGI_APPLICATION = 'business_logic.WebSocket.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "auth_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Channel Layers Configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Add ASGI application
ASGI_APPLICATION = 'auth_system.asgi.application'

WSGI_APPLICATION = "auth_system.wsgi.application"



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# SETTINGS FOR HOMEBREW  POSTGRESQL DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb',
        'USER': 'admin1',
        'PASSWORD': '123123',
        # 'HOST': 'db',  #  FOR docker-compose 
        'HOST': 'localhost',  # DEFAULT
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'testdb2',
#         'USER': 'meric',
#         'PASSWORD': '123123',
#     }
# }




# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
    ]

SOCIALACCOUNT_PROVIDERS = {
   'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
}

RECAPTCHA_PUBLIC_KEY = '_KEY'
RECAPTCHA_PRIVATE_KEY = '_KEY'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'meric.winn.alp@gmail.com'
EMAIL_HOST_USER = 'meric.winn.alp@gmail.com'
EMAIL_HOST_PASSWORD = 'hjglycwtnuvqpoxo'
EMAIL_PORT = 587    
EMAIL_USE_TLS = True


PASSWORD_RESET_TIMEOUT = 14400

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

