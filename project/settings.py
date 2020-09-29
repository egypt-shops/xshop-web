"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ
import sentry_sdk

from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# django-environ
env = environ.Env(
    # # set casting, default value
    # DEBUG=(bool, False)
)

# Deploy NOTE defined first to decide when to read the .env file
DEPLOY = env("DEPLOY", str, None)

# reading .env file ()
if not DEPLOY or DEPLOY == "LOCAL":
    environ.Env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS", tuple, ("localhost", "127.0.0.1", ".shahwan.me", ".herokuapp.com")
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "django_extensions",
    "phonenumber_field",
    "rest_framework",
    "rest_framework.authtoken",
    # Local
    "xshop.users.apps.UsersConfig",
    "xshop.pages.apps.PagesConfig",
    "xshop.core.apps.CoreConfig",
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "TEST": {"NAME": "xshop_test_db"},
        "CONN_MAX_AGE": 60 if DEPLOY != "LOCAL" else 0,
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (BASE_DIR / "static",)

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# PhoneNumber settings
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "EG"

# user model
AUTH_USER_MODEL = "users.User"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# sentry
if DEPLOY != "LOCAL":
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", str),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
