from .base import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=django,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "25001",
    },
    "data": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=development,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "25001",
    },
}

RABBIT = {
    "host": "localhost",
    "port": "25002",
    "username": "rabbit",
    "password": "rabbit",
    "exchange_name": "dqt_development",
}
