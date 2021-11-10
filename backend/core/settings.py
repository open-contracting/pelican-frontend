"""
Django settings for the project.

Generated by "django-admin startproject" using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
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
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "w^pq&p1phz$^1j!aqa#8zm#m@_jhm(9skcx*8rom7x7j1cy1y=")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not production

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0"]
if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS.extend(os.getenv("ALLOWED_HOSTS").split(","))


# Application definition

INSTALLED_APPS = [
    # tastypie depends on django.contrib.auth
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "tastypie",
    "corsheaders",
    "dqt",
    "controller.apps.ControllerConfig",
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default="postgresql:///pelican_frontend?application_name=pelican_frontend"),
    # The connection string for Pelican backend's database.
    "data": dj_database_url.config(
        env="PELICAN_BACKEND_DATABASE_URL", default="postgresql:///pelican_backend?application_name=pelican_frontend"
    ),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Project-specific Django configuration

LOCALE_PATHS = glob(str(BASE_DIR / "**" / "locale"))

STATIC_ROOT = BASE_DIR / "static"

# https://docs.djangoproject.com/en/3.2/topics/logging/#django-security
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
            "level": "INFO",
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

# https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
if production and not local_access:
    # Run: env DJANGO_ENV=production SECURE_HSTS_SECONDS=1 ./manage.py check --deploy
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = "same-origin"  # default in Django >= 3.1

    # https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security
    if "SECURE_HSTS_SECONDS" in os.environ:
        SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS"))
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

DATABASE_ROUTERS = ["dqt.routers.DbRouter"]


# Dependency configuration

if "SENTRY_DSN" in os.environ:
    # https://docs.sentry.io/platforms/python/logging/#ignoring-a-logger
    ignore_logger("django.security.DisallowedHost")
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0,  # The Sentry plan does not include Performance.
    )

if "CORS_ALLOWED_ORIGINS" in os.environ:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(",")
elif not production:
    CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}


# Project configuration

FATHOM = {
    "domain": os.getenv("FATHOM_ANALYTICS_DOMAIN") or "cdn.usefathom.com",
    "id": os.getenv("FATHOM_ANALYTICS_ID"),
}

# The path to a Google `credentials.json` file
# https://developers.google.com/workspace/guides/create-credentials
TOKEN_PATH = os.getenv("TOKEN_PATH", "credentials.json")

# The connection string for RabbitMQ.
RABBIT_URL = os.getenv("RABBIT_URL", "amqp://localhost")
# The name of the RabbitMQ exchange. Follow the pattern `pelican_{service}_{environment}`.
RABBIT_EXCHANGE_NAME = os.getenv("RABBIT_EXCHANGE_NAME", "pelican_development")

GDOCS_TEMPLATES = {
    # The Google Docs ID for the base template.
    "DEFAULT_BASE_TEMPLATE": os.getenv("DEFAULT_BASE_TEMPLATE", "1YMG5KZCPmI6GEcd2XQktrHD8uxEL626g3uuBjLWqQlE"),
    # The Google Docs ID for the field-level template.
    "DEFAULT_DATASET_TEMPLATE": os.getenv("DEFAULT_DATASET_TEMPLATE", "1_1FIg3cuUthk6EEWcYnR5S-J3Xx8p1ZVDBh5oZM3eK8"),
    # The Google Docs ID for the resource-level template.
    "DEFAULT_FIELD_TEMPLATE": os.getenv("DEFAULT_FIELD_TEMPLATE", "1DCYMTwh_cXt-kpuxEnyKMfTlmdUoc8MwUWgbgWj7fAA"),
    # The Google Docs ID for the dataset-level template.
    "DEFAULT_RESOURCE_TEMPLATE": os.getenv(
        "DEFAULT_RESOURCE_TEMPLATE", "1dX4md9MGOxhngjQ2Q0wY8njNiq5B6F9oFWd1tUN63TM"
    ),
    # The Google Docs ID for the error template.
    "DEFAULT_ERROR_TEMPLATE": os.getenv("DEFAULT_ERROR_TEMPLATE", "1PW7s6SmaP4tia_QzMSZkTt8Oii-6ZXqB7VCuF8bYmv4"),
}
