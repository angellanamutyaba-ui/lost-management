""" 
Django settings for lost_management project. 
""" 
 
from pathlib import Path 
import os 
 
BASE_DIR = Path(__file__).resolve().parent.parent 
 
SECRET_KEY = 'django-insecure-5(r0emt9te#g2l2n-b2zkboc2ixa1xe)hy07zq*fc$xm+4)gf' 
 
DEBUG = True 
 
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', 'lost-management.onrender.com'] 
 
INSTALLED_APPS = [ 
    'jazzmin', 
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
    'system', 
] 
 
MIDDLEWARE = [ 
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
] 
 
ROOT_URLCONF = 'lost_management.urls' 
 
TEMPLATES = [ 
    { 
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True, 
        'OPTIONS': { 
            'context_processors': [ 
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages', 
            ], 
        }, 
    }, 
] 
 
WSGI_APPLICATION = 'lost_management.wsgi.application' 
 
DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': BASE_DIR / 'db.sqlite3', 
    } 
} 
 
AUTH_PASSWORD_VALIDATORS = [ 
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, 
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, 
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, 
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}, 
] 
 
LANGUAGE_CODE = 'en-us' 
TIME_ZONE = 'UTC' 
USE_I18N = True 
USE_TZ = True 
 
STATIC_URL = '/static/' 
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [BASE_DIR / 'static',] 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
 
MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media' 
 
LOGIN_URL = '/login/' 
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGOUT_REDIRECT_URL = '/' 
 
if not os.path.exists(MEDIA_ROOT): 
    os.makedirs(MEDIA_ROOT) 
 
JAZZMIN_SETTINGS = { 
    "site_title": "Lost Management System", 
    "site_header": "LMS Admin", 
    "site_brand": "Lost Management", 
    "welcome_sign": "Welcome to Lost Management System", 
} 
