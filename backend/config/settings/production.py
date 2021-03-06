from .base import *  # NOQA

# ----------------------------------------------------
# *** Allowed Hosts ***
# ----------------------------------------------------

ALLOWED_HOSTS = ["mysite.example.com"]

# ----------------------------------------------------
# *** Databases ***
# ----------------------------------------------------

DATABASES = {'default': get_env_value('DATABASE_URL')}  # NOQA
# set atomic requests
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # NOQA

# ----------------------------------------------------
# *** Debug ***
# ----------------------------------------------------

DEBUG = False

# ----------------------------------------------------
# *** Templates ***
# ----------------------------------------------------

TEMPLATES[0]["DIRS"] = [os.path.join(root.path(), "templates")]  # NOQA

# ----------------------------------------------------
# *** CACHES ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#caches

CACHES = {
    'default': {
        # https://github.com/django-pymemcache/django-pymemcache
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'rosetta': {
        # https://github.com/django-pymemcache/django-pymemcache
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# ----------------------------------------------------
# *** LOGGING ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details on
# how to customize logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# ----------------------------------------------------
# *** Others ***
# ----------------------------------------------------

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env.str("DJANGO_ADMIN_URL")  # NOQA

# ==============================================================================
# *** SECURITY SETTINGS ***
# ==============================================================================

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # NOQA
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once
# you prove the former works
SECURE_HSTS_SECONDS = 60  # 60 * 60 * 24 * 7 * 52  # one year
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(  # NOQA
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)  # NOQA
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(  # NOQA
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True


# ----------------------------------------------------
# *** --------------- Third Party --------------- ***
# ----------------------------------------------------

# ----------------------------------------------------
# *** Django Cors Headers ***
# ----------------------------------------------------

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://mysite.example.com',
)

# ----------------------------------------------------
# *** Django Compressor ***
# ----------------------------------------------------

# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_ENABLED#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)  # NOQA
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_URL#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL  # NOQA
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE
# Offline compression is required when using Whitenoise
COMPRESS_OFFLINE = True
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE_TIMEOUT
COMPRESS_OFFLINE_TIMEOUT = 31536000  # 1 year
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_FILTERS#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}


# ----------------------------------------------------
# *** Django Cleanup (Place to the bottom) ***
# NOTE: Needs to be placed at the bottom of INSTALLED_APPS
# ----------------------------------------------------

if "django_cleanup.apps.CleanupConfig" not in INSTALLED_APPS:  # NOQA
    INSTALLED_APPS.insert(-1, "django_cleanup.apps.CleanupConfig")  # NOQA
