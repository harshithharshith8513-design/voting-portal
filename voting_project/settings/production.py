import os
from decouple import config, Csv
import dj_database_url
from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Dynamic ALLOWED_HOSTS handling
ALLOWED_HOSTS = []

# Add from environment variable if present
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS.extend([host.strip() for host in allowed_hosts_env.split(',') if host.strip()])

# Add Render's built-in hostname
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

# Fallback hosts for common cases
ALLOWED_HOSTS.extend([
    'voting-portal-2.onrender.com',
    '.onrender.com',  # Wildcard for all Render subdomains
])

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
