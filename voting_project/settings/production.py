from .base import *
import os
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com']

# Database
DATABASES = {
    'default': dj_database_url.config(
        defaimport os
from decouple import config, Csv
from .base import *

# Debug prints (remove after fixing)
print(f"DEBUG: Using settings module: {os.environ.get('DJANGO_SETTINGS_MODULE', 'Not Set')}")

# Essential settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS - Multiple approaches for reliability
ALLOWED_HOSTS = []

# Method 1: Parse from environment variable
try:
    allowed_hosts_env = config('ALLOWED_HOSTS', default='', cast=Csv())
    if allowed_hosts_env:
        ALLOWED_HOSTS.extend(allowed_hosts_env)
        print(f"DEBUG: Loaded from env: {allowed_hosts_env}")
except Exception as e:
    print(f"DEBUG: Error parsing ALLOWED_HOSTS: {e}")

# Method 2: Add Render's built-in hostname
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    print(f"DEBUG: Added Render hostname: {render_hostname}")

# Method 3: Hardcoded fallbacks
ALLOWED_HOSTS.extend([
    'voting-portal-2.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
])

# Remove duplicates and empty values
ALLOWED_HOSTS = list(set([host for host in ALLOWED_HOSTS if host]))
print(f"DEBUG: Final ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# SQLite Database (since you're using SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
ult=os.environ.get('DATABASE_URL')
    )
}

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
