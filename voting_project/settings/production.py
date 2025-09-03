import os
import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

# Handle ALLOWED_HOSTS from environment variable
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '')
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS.split(',')]
else:
    ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
