"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# import os
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

# reading .env file () when testing and in LOCAL env else read from env vars
if not DEPLOY or DEPLOY == "LOCAL":
    environ.Env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS",
    tuple,
    ("localhost", "127.0.0.1", ".shahwan.me", ".herokuapp.com", ".ngrok.io"),
)


# Application definition

# NOTE that Somtimes order matters
INSTALLED_APPS = [
    # Third party
    "baton",
    # Built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "phonenumber_field",
    "multiselectfield",
    "crispy_forms",
    "crispy_tailwind",
    "djmoney",
    "drf_spectacular",
    # Local
    "xshop.users.apps.UsersConfig",
    "xshop.pages.apps.PagesConfig",
    "xshop.core.apps.CoreConfig",
    "xshop.shops.apps.ShopsConfig",
    "xshop.products.apps.ProductsConfig",
    "xshop.orders.apps.OrdersConfig",
    "xshop.invoices.apps.InvoicesConfig",
    "xshop.cart.apps.CartConfig",
    "xshop.payments.apps.PaymentsConfig",
    # Third party
    "baton.autodiscover",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
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
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Login & Redirection
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "users:redirection"
LOGOUT_REDIRECT_URL = "pages:home"

# Cart Session ID
CART_SESSION_ID = "cart"
CURRENT_SHOP_SESSION_ID = "current_shop"

# sentry
if DEPLOY and DEPLOY not in ("LOCAL", "TESTING"):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", str),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# TODO update using existing models in all apps, or whatever suitable!
# FIXME you might depend only on permissions and deprecate this w 5las!
DASHBOARD_MODULES = []

# django-money
CURRENCIES = ("EGP",)
CURRENCY_CHOICES = [
    ("EGP", "EGP E£"),
]
DEFAULT_CURRENCY = "EGP"
CURRENCY_DECIMAL_PLACES = 2

# All URLs end with '/'
APPEND_SLASH = True

# https://drf-spectacular.readthedocs.io/en/latest/settings.html#django-rest-framework-settings
SPECTACULAR_SETTINGS = {
    "TITLE": "XShop Web API",
    "DESCRIPTION": "API for XShop web to be integrated with mobile application and website",
    "VERSION": "1.0.0",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    # A regex specifying the common denominator for all operation paths. If
    # SCHEMA_PATH_PREFIX is set to None, drf-spectacular will attempt to estimate
    # a common prefix. use '' to disable.
    # Mainly used for tag extraction, where paths like '/api/v1/albums' with
    # a SCHEMA_PATH_PREFIX regex '/api/v[0-9]' would yield the tag 'albums'.
    "SCHEMA_PATH_PREFIX": "api/",
}

# PayMob
PAYMOB_API_KEY = env("PAYMOB_API_KEY")
PAYMOB_IFRAME_ID = env("PAYMOB_IFRAME_ID")
PAYMOB_CARD_INTEGRATION_ID = env("PAYMOB_CARD_INTEGRATION_ID")


# Django admin customization with Baton
BATON = {
    "SITE_HEADER": "Egypt Shops",
    "SITE_TITLE": "Egypt Shops",
    "INDEX_TITLE": "Administration",
    "SUPPORT_HREF": "https://egypt-shops.github.io/",
    "COPYRIGHT": "copyright © 2020 <a href='https://egypt-shops.github.io/'>Egypt Shops</a>",
    "POWERED_BY": "<a href='https://egypt-shops.github.io/'>Egypt Shops</a>",
    "CONFIRM_UNSAVED_CHANGES": True,
    "SHOW_MULTIPART_UPLOADING": True,
    "ENABLE_IMAGES_PREVIEW": True,
    "CHANGELIST_FILTERS_IN_MODAL": True,
    "CHANGELIST_FILTERS_ALWAYS_OPEN": False,
    "COLLAPSABLE_USER_AREA": False,
    "MENU_ALWAYS_COLLAPSED": False,
    "MENU_TITLE": "Menu",
    "GRAVATAR_DEFAULT_IMG": "retro",
    "MENU": (
        {"type": "title", "label": "System", "apps": ("auth", "users")},
        # {
        #     "type": "app",
        #     "name": "auth",
        #     "label": "Authentication",
        #     "icon": "fa fa-lock",
        #     "models": (
        #         # {"name": "user", "label": "Users"},
        #         {"name": "group", "label": "Groups"},
        #     ),
        # },
        {"type": "model", "label": "Users", "name": "user", "app": "users"},
        {"type": "model", "label": "Groups", "name": "group", "app": "auth"},
        {"type": "title", "label": "Shop", "apps": ("shops", "users")},
        {
            "type": "free",
            "label": "Users",
            "apps": ("users", "shops"),
            "default_open": False,
            "children": [
                {
                    "type": "model",
                    "label": "General Managers",
                    "name": "generalmanager",
                    "app": "users",
                },
                {
                    "type": "model",
                    "label": "Managers",
                    "name": "manager",
                    "app": "users",
                },
                {
                    "type": "model",
                    "label": "Cashiers",
                    "name": "cashier",
                    "app": "users",
                },
                {
                    "type": "model",
                    "label": "Data Entry Clerks",
                    "name": "dataentryclerk",
                    "app": "users",
                },
                {
                    "type": "model",
                    "label": "Customers",
                    "name": "customer",
                    "app": "users",
                },
            ],
        },
        # {
        #     "type": "app",
        #     "name": "users",
        #     "label": "Users",
        #     "icon": "fa fa-users",
        #     "models": ({"name": "user", "label": "Users"},),
        # },
        # {
        #     "type": "app",
        #     "name": "users",
        #     "label": "Users",
        #     "icon": "fa fa-users",
        #     "models": (
        #         {"name": "Cashier", "label": "Cashiers"},
        #         {"name": "User", "label": "users"},
        #     ),
        # },
        # {"type": "title", "label": "main", "apps": ("auth",)},
        # {
        #     "type": "app",
        #     "name": "auth",
        #     "label": "Authentication",
        #     "icon": "fa fa-lock",
        #     "models": (
        #         {"name": "user", "label": "Users"},
        #         {"name": "group", "label": "Groups"},
        #     ),
        # },
        # {"type": "title", "label": "Contents", "apps": ("flatpages",)},
        # {"type": "model", "label": "Pages", "name": "flatpage", "app": "flatpages"},
        # {
        #     "type": "free",
        #     "label": "Custom Link",
        #     "url": "http://www.google.it",
        #     "perms": ("flatpages.add_flatpage", "auth.change_user"),
        # },
        # {
        #     "type": "free",
        #     "label": "Users",
        #     "default_open": True,
        #     "children": [
        #         {
        #             "type": "model",
        #             "label": "Users",
        #             "name": "user",
        #             "app": "xshop.users",
        #         },
        #         # {
        #         #     "type": "free",
        #         #     "label": "Another custom link",
        #         #     "url": "http://www.google.it",
        #         # },
        #     ],
        # },
    ),
    # "ANALYTICS": {
    #     "CREDENTIALS": os.path.join(BASE_DIR, "credentials.json"),
    #     "VIEW_ID": "12345678",
    # },
}
