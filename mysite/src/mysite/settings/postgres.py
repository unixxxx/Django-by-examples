import os
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', None),
        'USER': os.environ.get('USER_NAME', None),
        'PASSWORD': os.environ.get('PASSWORD', None)
    }
}

INSTALLED_APPS += [
    'django.contrib.postgres'
]
