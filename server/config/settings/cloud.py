"""HTTPS cloud testing with PostgreSQL and same-origin frontend proxy."""
from .base import *
import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
DEBUG = False
SECRET_KEY = env('DJANGO_SECRET_KEY')
if len(SECRET_KEY) < 50 or SECRET_KEY.startswith('django-insecure'):
    raise ImproperlyConfigured('DJANGO_SECRET_KEY precisa de pelo menos 50 caracteres aleatórios.')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
for value in (os.environ.get('RENDER_EXTERNAL_HOSTNAME'), os.environ.get('VERCEL_URL')):
    if value and value not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(value)
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('Defina DJANGO_ALLOWED_HOSTS com os hosts exatos do frontend e backend.')
DATABASES = {'default': env.db('DATABASE_URL')}
if DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql':
    raise ImproperlyConfigured('Use PostgreSQL persistente no ambiente cloud.')
DATABASES['default']['CONN_MAX_AGE'] = 0
FRONTEND_URL = env('FRONTEND_URL').rstrip('/')
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[FRONTEND_URL])
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys([FRONTEND_URL, *CORS_ALLOWED_ORIGINS]))
CSRF_TRUSTED_ORIGINS += [f'https://{host}' for host in ALLOWED_HOSTS if not host.startswith('.')]
AUTH_COOKIE_SECURE = CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = True
AUTH_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 3600
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
MIDDLEWARE = [MIDDLEWARE[0], MIDDLEWARE[1], 'whitenoise.middleware.WhiteNoiseMiddleware', *MIDDLEWARE[2:]]
STORAGES = {'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
            'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
if not os.environ.get('REDIS_URL'):
    CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@fluidmes.example')
