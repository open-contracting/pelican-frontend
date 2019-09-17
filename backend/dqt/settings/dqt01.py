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
