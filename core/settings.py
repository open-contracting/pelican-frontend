"""
Django settings for the project.

Generated by "django-admin startproject" using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from glob import glob
from pathlib import Path

import dj_database_url
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

production = os.getenv("DJANGO_ENV") == "production"
local_access = "LOCAL_ACCESS" in os.environ or "ALLOWED_HOSTS" not in os.environ

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "w^pq&p1phz$^1j!aqa#8zm#m@_jhm(9skcx*8rom7x7j1cy1y=")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", str(not production)) == "True"

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0"]  # noqa: S104 # Docker
if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS.extend(os.getenv("ALLOWED_HOSTS").split(","))


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    "api.apps.APIConfig",
    "exporter.apps.ExporterConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default="postgresql:///pelican_frontend?application_name=pelican_frontend"),
    # The connection string for Pelican backend's database.
    "pelican_backend": dj_database_url.config(
        env="PELICAN_BACKEND_DATABASE_URL",
        default="postgresql:///pelican_backend?application_name=pelican_frontend",
    ),
    "kingfisher_process": dj_database_url.config(
        env="KINGFISHER_PROCESS_DATABASE_URL",
        default="postgresql:///kingfisher_process?application_name=pelican_frontend",
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Project-specific Django configuration

LOCALE_PATHS = glob(str(BASE_DIR / "**" / "locale"))

STATIC_ROOT = BASE_DIR / "static"

# https://docs.djangoproject.com/en/4.2/topics/logging/#django-security
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL", "INFO"),
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if production else os.getenv("LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        # Never show DEBUG messages.
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
if production and not local_access:
    # Run: env DJANGO_ENV=production SECURE_HSTS_SECONDS=1 ./manage.py check --deploy
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = "same-origin"  # default in Django >= 3.1

    # https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security
    if "SECURE_HSTS_SECONDS" in os.environ:
        SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS"))
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

# https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header
if "DJANGO_PROXY" in os.environ:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

DATABASE_ROUTERS = ["api.routers.DbRouter"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/data" if production else "",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Dependency configuration

if "SENTRY_DSN" in os.environ:
    # https://docs.sentry.io/platforms/python/logging/#ignoring-a-logger
    ignore_logger("django.security.DisallowedHost")
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
    )

if "CORS_ALLOWED_ORIGINS" in os.environ:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(",")
elif not production:
    CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# Project configuration

FATHOM = {
    "domain": os.getenv("FATHOM_ANALYTICS_DOMAIN") or "cdn.usefathom.com",
    "id": os.getenv("FATHOM_ANALYTICS_ID"),
}

# The connection string for RabbitMQ.
RABBIT_URL = os.getenv("RABBIT_URL", "amqp://127.0.0.1")
# The name of the RabbitMQ exchange used by Pelican backend.
RABBIT_EXCHANGE_NAME = os.getenv("RABBIT_EXCHANGE_NAME", "pelican_development")

# The path to a service account JSON file, for writing exports to Google Drive.
# https://developers.google.com/workspace/guides/create-credentials#service-account
SERVICE_ACCOUNT_JSON_FILE = os.getenv("SERVICE_ACCOUNT_JSON_FILE", "credentials.json")

# The Google Docs IDs for templates, when writing exports to Google Drive.
GDOCS_TEMPLATES = {
    # The Google Docs ID for the base template.
    "DEFAULT_BASE_TEMPLATE": os.getenv("DEFAULT_BASE_TEMPLATE", "1jSGZKNJP6wBVPwi3JsvdkZ9FSpUwrK2SJxZoQQuJdnM"),
    "DEFAULT_BASE_TEMPLATE_ES": os.getenv("DEFAULT_BASE_TEMPLATE_ES", "1DOxUeeUUjNPxAKu04etMBWyRbKkn8C1ZCskpeXUKJSg"),
    # The Google Docs ID for the overview template.
    "DEFAULT_OVERVIEW_TEMPLATE": os.getenv(
        "DEFAULT_OVERVIEW_TEMPLATE", "1sYr5LipKRtegWWl3zfKIDoSZmZluawmAdAu3piKslTw"
    ),
    # The Google Docs ID for the field-level template.
    "DEFAULT_FIELD_TEMPLATE": os.getenv("DEFAULT_FIELD_TEMPLATE", "1We-5SJ7i8i-d0c7U8t9QRstf0EHkn5zQeVh5UfDkb2c"),
    # The Google Docs ID for the resource-level template.
    "DEFAULT_RESOURCE_TEMPLATE": os.getenv(
        "DEFAULT_RESOURCE_TEMPLATE", "1bnfFXZ3AYjXc--u9ohM9KTGwo05dz7BJmh4KIDdzalc"
    ),
    # The Google Docs ID for the dataset-level template.
    "DEFAULT_DATASET_TEMPLATE": os.getenv("DEFAULT_DATASET_TEMPLATE", "1CBVNkHE4WJCXCkSZlDgL6qDoLFJhcCvln8jvTEyZh_k"),
    # The Google Docs ID for the error template.
    "DEFAULT_ERROR_TEMPLATE": os.getenv("DEFAULT_ERROR_TEMPLATE", "1PW7s6SmaP4tia_QzMSZkTt8Oii-6ZXqB7VCuF8bYmv4"),
}
GOOGLE_DRIVE_USER = os.getenv("GOOGLE_DRIVE_USER", "")
GOOGLE_DRIVE_FOLDER = "1ZVwf9cr29E4uCuWaVRiQLJI7_ejE00h3"
