from .base import *

CORS_ORIGIN_WHITELIST = (
    'dqt.datlab.eu',
    'localhost:22005'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,public'
        },
        'NAME': 'dqt',
        'USER': 'dqt',
        'PASSWORD': 'dqt',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },

    'data': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=production,public'
        },
        'NAME': 'dqt',
        'USER': 'dqt',
        'PASSWORD': 'dqt',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}

RABBIT = {
    "host": "localhost",
    "port": "5672",
    "username": "rabbit",
    "password": "rabbit",
    "exchange_name": "dqt_production",
}
