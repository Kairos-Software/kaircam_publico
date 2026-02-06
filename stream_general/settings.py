import os
from pathlib import Path
from dotenv import load_dotenv

# ============================
# BASE DIR
# ============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# ENVIRONMENT
# ============================
ENV = os.getenv("ENV", "local")

env_file = BASE_DIR / f".env.{ENV}"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(BASE_DIR / ".env")

# ============================
# SECURITY
# ============================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-key")

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# ============================
# APPLICATIONS
# ============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'principal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stream_general.urls'

# ============================
# TEMPLATES
# ============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'stream_general.wsgi.application'
ASGI_APPLICATION = 'stream_general.asgi.application'

# ============================
# DATABASE
# ============================
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}

# ============================
# PASSWORD VALIDATION
# ============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================
# I18N
# ============================
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# ============================
# STATIC FILES
# ============================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================
# HLS SETTINGS (PÚBLICO)
# ============================
HLS_BASE_URL = os.getenv("HLS_BASE_URL")
HLS_PROGRAM_PATH = os.getenv("HLS_PROGRAM_PATH", "program")


CSRF_TRUSTED_ORIGINS = ['https://kaircam.grupokairosarg.com/']
SESSION_COOKIE_SECURE = True  # Solo si usas HTTPS
CSRF_COOKIE_SECURE = True     # Solo si usas HTTPS