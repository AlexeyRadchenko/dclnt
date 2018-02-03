import os
from .my_config_vars import MY_SECRET_KEY, MY_USERS_PASS
from configurations import Configuration, values


class BASE(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = MY_SECRET_KEY
    DEBUG = True
    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'debug_toolbar',
        'counters',
        'management',
        'rest_framework',
        'api_v0',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    ROOT_URLCONF = 'Project.urls'

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

    WSGI_APPLICATION = 'Project.wsgi.application'

    DATABASES = values.DatabaseURLValue('sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'),
                                        environ=True)

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

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

    LANGUAGE_CODE = 'ru-RU'

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = False

    USE_TZ = True

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    MEDIA_URL = '/media/'

    FILE_UPLOAD_HANDLERS = [
        'django.core.files.uploadhandler.MemoryFileUploadHandler',
        'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    ]
    # REDIS settings
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'

    CACHES = values.CacheURLValue(f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

    # CELERY settings
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

    DATE_FORMAT = '%d.%m.%Y'
    USERS_PASS = MY_USERS_PASS

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
        # '...
    }

class Dev(BASE):
    INTERNAL_IPS = [
        '127.0.0.1'
    ]


class Prod(BASE):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
