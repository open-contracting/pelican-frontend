from .base import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=django,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "33002",
    },
    "data": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=development,public"},
        "NAME": "dqt",
        "USER": "dqt",
        "PASSWORD": "dqt",
        "HOST": "127.0.0.1",
        "PORT": "33002",
    },
}
