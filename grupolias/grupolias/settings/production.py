from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "grupolias.com,www.grupolias.com").split(",")

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", "db"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}

# Seguridad básica para producción
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Wagtail
WAGTAILADMIN_BASE_URL = os.getenv("BASE_URL", "https://grupolias.com")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

TURNSTILE_SITEKEY = os.getenv("TURNSTILE_SITEKEY")
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")

try:
    from .local import *
except ImportError:
    pass
