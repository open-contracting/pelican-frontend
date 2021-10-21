import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F401, F403

DEBUG = os.getenv("DEBUG", "NO").lower() in ("on", "true", "y", "yes", "1")

ALLOWED_HOSTS = ["*"]

if os.getenv("SENTRY_DSN", False):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0,  # The Sentry plan does not include Performance.
    )

CORS_ORIGIN_WHITELIST = (os.getenv("CORS_ORIGIN_WHITELIST"),)

SECRET_KEY = os.getenv("SECRET_KEY", "sesdkfhj87y149erwbgh")

TOKEN_PATH = os.getenv("TOKEN_PATH", "/data/credentials.json")

DATABASES = {
    "default": dj_database_url.config(default="postgresql:///pelican_frontend?application_name=pelican_frontend"),
    "data": dj_database_url.config(
        env="PELICAN_BACKEND_DATABASE_URL", default="postgresql:///pelican_backend?application_name=pelican_backend"
    ),
}

RABBIT = {
    "host": os.getenv("RABBIT_HOST"),
    "port": os.getenv("RABBIT_PORT"),
    "username": os.getenv("RABBIT_USERNAME"),
    "password": os.getenv("RABBIT_PASSWORD"),
    "exchange_name": os.getenv("RABBIT_EXCHANGE_NAME"),
}

GDOCS_TEMPLATES = {
    "DEFAULT_BASE_TEMPLATE": os.getenv("DEFAULT_BASE_TEMPLATE"),
    "DEFAULT_DATASET_TEMPLATE": os.getenv("DEFAULT_DATASET_TEMPLATE"),
    "DEFAULT_FIELD_TEMPLATE": os.getenv("DEFAULT_FIELD_TEMPLATE"),
    "DEFAULT_RESOURCE_TEMPLATE": os.getenv("DEFAULT_RESOURCE_TEMPLATE"),
    "DEFAULT_ERROR_TEMPLATE": os.getenv("DEFAULT_ERROR_TEMPLATE"),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "data_registry": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "exporter": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "cbom": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "scrape-task": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
