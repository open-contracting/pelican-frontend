from .base import *

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
        'PORT': '22002',
    },

    'data': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=development,public'
        },
        'NAME': 'dqt',
        'USER': 'dqt',
        'PASSWORD': 'dqt',
        'HOST': '127.0.0.1',
        'PORT': '22002',
    },
}

RABBIT = {
    "host": "localhost",
    "port": "22000",
    "username": "rabbit",
    "password": "rabbit",
    "exchange_name": "dqt_development",
}
