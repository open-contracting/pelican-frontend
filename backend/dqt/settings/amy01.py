from .base import *  # noqa: F401, F403

CORS_ORIGIN_WHITELIST = ("https://pelican.datlab.eu")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=django,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
    "data": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=production,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
}

RABBIT = {
    "host": "localhost",
    "port": "5672",
    "username": "rabbit",
    "password": "rabbit",
    "exchange_name": "dqt_production",
}
