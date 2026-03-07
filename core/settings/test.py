from .base import *

DEBUG = False

# Use in-memory cache instead of Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}

# Faster password hashing in tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable throttling during tests
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}