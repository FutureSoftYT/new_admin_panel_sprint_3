import os
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

if ALLOWED_HOSTS := os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]']

include(
    'components/database.py',
    'components/apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/auth_path_validator.py'
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LOCALE_PATHS = ['movies/locale']

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
