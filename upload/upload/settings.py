import os
import djcelery
djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Core applications of Django
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third Party Applications
THIRD_PARTY_APPS = [
    'djcelery',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
]

# Aplicaciones Locales
LOCAL_APPS = [
    'apps.tickets',
]

# Installed Project Applications
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'upload.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'upload.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME'    : os.environ['DATABASE_NAME'],
        'USER'    : os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST'    : os.environ['DATABASE_HOST'],
        'PORT'    : os.environ['DATABASE_PORT'],
    }
}

# Password validation
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

BROKER_URL = 'django://'
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_BROKER_URL = 'amqp://localhost'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload.settings')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Internationalization
LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]+['static'])
STATIC_URL  = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'upload/static'),
]

MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(BASE_DIR, "upload/media")

"""
DEFAULT_FILE_STORAGE = os.environ['DEFAULT_FILE_STORAGE']
STATICFILES_STORAGE = os.environ['DEFAULT_FILE_STORAGE']

# Amazon S3 - AWS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# Google Cloud Storage
GS_PROJECT_ID = os.environ['GS_PROJECT_ID']
GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']
GS_CREDENTIALS = os.environ['GS_CREDENTIALS']
PRIVATE_KEY_ID = os.environ['PRIVATE_KEY_ID']
PRIVATE_KEY = PRIVATE_KEY

# Dropbox
DROPBOX_OAUTH2_TOKEN=os.environ['DROPBOX_OAUTH2_TOKEN']
"""
