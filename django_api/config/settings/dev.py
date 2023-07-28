from .base import *

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}},
    'formatters': {'default': {'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'}},
    'handlers': {
        'debug-console': {'class': 'logging.StreamHandler', 'formatter': 'default', 'filters': ['require_debug_true'],},
    },
    'loggers': {'django.db.backends': {'level': 'DEBUG', 'handlers': ['debug-console'], 'propagate': False,}},
}