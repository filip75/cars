from cars.settings.common import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "mydatabase",}}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache",}}
