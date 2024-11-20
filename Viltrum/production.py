"""
Django settings for Viltrum project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
from django.urls import reverse_lazy

# Claves de API (descomenta si necesitas usarlas)
# API_KEY_STEAM = config('API_KEY_STEAM')
# API_KEY_RIOT = config('API_KEY_RIOT')

# Configuración del correo electrónico


# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones rápidas para desarrollo (ajusta en producción)
SECRET_KEY = os.environ['SECRET']

DEBUG = False

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 'viltrum.es']
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME'], 'https://viltrum.es']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'daphne',
    'taggit',
    'storages',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'tournaments.apps.TournamentsConfig',
    'clasifications.apps.ClasificationsConfig',
    'explore.apps.ExploreConfig',
    'sponsors.apps.SponsorsConfig',
    'notifications.apps.NotificationsConfig',
    'chat.apps.ChatConfig',
    'shop.apps.ShopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
]

# Configuración de autenticación y redirección
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Manejo de mensajes
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Configuración de URLs y ASGI
ROOT_URLCONF = 'Viltrum.urls'
ASGI_APPLICATION = "Viltrum.asgi.application"

# Configuración de plantillas
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
                'core.context_processors.user_role',
                'core.context_processors.notifications',
                'core.context_processors.verification',
                'core.context_processors.profile_img'
            ],
        },
    },
]

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'viltrum',
        'USER': 'viltrumadmin',
        'PASSWORD': os.environ['AIVEN_PASSWORD'],
        'HOST': 'mysql-106b7d30-lasallistas-05c9.b.aivencloud.com',
        'PORT': '24980',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'certificates', 'ca.pem'),
            }
        }
    }
}


# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y de medios
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
 
STATICFILES_DIRS = (str(BASE_DIR.joinpath('azure_content/static')),)
STATIC_URL = '/azure_content/static/'

#Media
DEFAULT_FILE_STORAGE = 'backend.custom_azure.AzureMediaStorage'
 
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = os.environ.get('AZURE_MEDIA_CONTAINER', 'media')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

MEDIA_LOCATION = "media"
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sviltrum@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = 'no-reply@viltrum.com'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f"rediss://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_SERVER']}:6380"],
        },
    },
}