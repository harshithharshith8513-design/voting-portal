import os
import dj_database_url
from .base import *

# TEMPORARY - Only for testing
ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

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
