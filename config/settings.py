from pathlib import Path
import os
import logging
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = config('SECRET_KEY')

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

# CELERY_BROKER_URL = 'redis://localhost:6379/0'  
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

DEBUG = True
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_twilio',
    # 'django_celery_beat',

    'users.apps.UsersConfig',
    'work_tower.apps.WorkTowerConfig',
    'task.apps.TaskConfig',
    'workflow.apps.WorkflowConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'users.context_processors.employee_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LANGUAGES = [
    ('uk', 'Ukrainian'),
    ('en', 'English'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

logging.basicConfig(level=logging.DEBUG)
LOGGING = {
    # 'version': 1,
    # 'disable_existing_loggers': False,
    # 'formatters': {
    #     'verbose': {
    #         'format': '{levelname} {asctime} {module} {message}',
    #         'style': '{',
    #     },
    # },
    # 'handlers': {
    #     'console': {
    #         'level': 'DEBUG',
    #         'class': 'logging.StreamHandler',
    #         'formatter': 'verbose',
    #     },
    #     'file': {
    #         'level': 'INFO',
    #         'class': 'logging.FileHandler',
    #         'filename': os.path.join(BASE_DIR, 'logs', 'application.log'),
    #         'formatter': 'verbose',
    #     },
    # },
    # 'loggers': {
    #     'django': {
    #         'handlers': ['console', 'file'],
    #         'level': 'INFO',
    #         'propagate': True,
    #     },
    #     '__main__': {
    #         'handlers': ['console', 'file'],
    #         'level': 'DEBUG',
    #         'propagate': False,
    #     },
    #     'users': {  
    #         'handlers': ['console', 'file'],
    #         'level': 'DEBUG',
    #     },
    # },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
