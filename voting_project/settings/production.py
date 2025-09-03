import os
from decouple import config, Csv
from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = []

# Parse from environment variable (comma-separated)
allowed_hosts_env = config('ALLOWED_HOSTS', default='', cast=Csv())
if allowed_hosts_env:
    ALLOWED_HOSTS.extend(allowed_hosts_env)

# Add Render's built-in hostname automatically
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

# Explicit fallbacks for your specific domain
ALLOWED_HOSTS.extend([
    'voting-portal-2.onrender.com',
    '.onrender.com',  # Wildcard for all Render subdomains
])

# Remove duplicates and empty values
ALLOWED_HOSTS = list(set([host for host in ALLOWED_HOSTS if host]))

# SQLite Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
