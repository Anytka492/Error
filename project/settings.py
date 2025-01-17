"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kx2uu#g49x(3fzia(dgssmrvt4z3(gn*ixl_)*r@_t^aq-#gc6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',
    'news',
    'django_filters',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
    'rest_framework',
    "rest_framework.authtoken",
    "rest_framework_simplejwt",

]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'news.middlewares.TimezoneMiddleware',


    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'project.urls'
LOGIN_REDIRECT_URL = "/news"

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'project.translation'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
SITE_URL = 'http://127.0.0.1:8000'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "antoshkina001"
EMAIL_HOST_PASSWORD = "wqeqfwadeochqtrf"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_ADMIN = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = "antoshkina001@yandex.com"
SERVER_EMAIL = "antoshkina001@yandex.com"


CELERY_BROKER_URL = 'redis://default:aUmInUIg8RGRceHELczA7ONi0IS2j9JA@redis-14676.c253.us-central1-1.gce.cloud.redislabs.com:14676'
CELERY_RESULT_BACKEND = 'redis://default:aUmInUIg8RGRceHELczA7ONi0IS2j9JA@redis-14676.c253.us-central1-1.gce.cloud.redislabs.com:14676'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'filters': ['require_debug_true']
        },
        'warning_handler': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'warning_formatter_style',
            'filters': ['require_debug_true']
        },
        'critical_handler': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'error_critical_formatter_style',
            'filters': ['require_debug_true']
        },
        'general_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'not_default_formatter',
            'filters': ['require_debug_false']
        },
        'errors_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'error_critical_formatter_style',
            'filters': ['require_debug_false']
        },
        'security_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'not_default_formatter',
            'filters': ['require_debug_false']
        },
        'send_admin_mail': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'error_critical_formatter_style',
            'filters': ['require_debug_false']
        }
    },
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'warning_formatter_style': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        },
        'error_critical_formatter_style': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'not_default_formatter': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
    },
    'style': '{',
    'loggers': {
            'django': {
                'handlers': ['console_handler', 'warning_handler', 'critical_handler', 'general_handler',],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['errors_handler', 'send_admin_mail',],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.server': {
                'handlers': ['errors_handler', 'send_admin_mail',],
                'propagate': True,
            },
            'django.template': {
                'handlers': ['errors_handler',],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': {
                'handlers': ['errors_handler',],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.security': {
                'handlers': ['security_log'],
                'level': 'INFO',
                'propagate': True,
            },

        },
}


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
