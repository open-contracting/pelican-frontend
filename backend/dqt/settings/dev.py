import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F401, F403

DEBUG = os.getenv("DEBUG", "NO").lower() in ("on", "true", "y", "yes", "1")

ALLOWED_HOSTS = ["*"]

if os.getenv("SENTRY_DNS", False):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DNS"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0,  # The Sentry plan does not include Performance.
    )

CORS_ORIGIN_WHITELIST = (os.getenv("CORS_ORIGIN_WHITELIST"),)

SECRET_KEY = os.getenv("SECRET_KEY", "sesdkfhj87y149erwbgh")

TOKEN_PATH = os.getenv("TOKEN_PATH", "/data/credentials.json")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path={}".format(os.getenv("DEFAULT_DB_SEARCH_PATH"))},
        "NAME": os.getenv("DEFAULT_DB_NAME"),
        "USER": os.getenv("DEFAULT_DB_USER"),
        "PASSWORD": os.getenv("DEFAULT_DB_PASSWORD"),
        "HOST": os.getenv("DEFAULT_DB_HOST"),
        "PORT": os.getenv("DEFAULT_DB_PORT"),
    },
    "data": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path={}".format(os.getenv("DATA_DB_SEARCH_PATH"))},
        "NAME": os.getenv("DATA_DB_NAME"),
        "USER": os.getenv("DATA_DB_USER"),
        "PASSWORD": os.getenv("DATA_DB_PASSWORD"),
        "HOST": os.getenv("DATA_DB_HOST"),
        "PORT": os.getenv("DATA_DB_PORT"),
    },
}

RABBIT = {
    "host": os.getenv("RABBIT_HOST"),
    "port": os.getenv("RABBIT_PORT"),
    "username": os.getenv("RABBIT_USERNAME"),
    "password": os.getenv("RABBIT_PASSWORD"),
    "exchange_name": os.getenv("RABBIT_EXCHANGE_NAME"),
}
