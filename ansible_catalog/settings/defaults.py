"""
Django settings for ansible_catalog project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import environ
import os
import sys
from pathlib import Path


env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Django gettext files path: locale/<lang-code>/LC_MESSAGES/django.po, django.mo
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-k8^atj4p3jj^zkb3=o(rhaysjzy_mr&#h(yl+ytj#f%@+er4&5"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CATALOG_API_PATH_PREFIX = env.str(
    "ANSIBLE_CATALOG_API_PATH_PREFIX", default="/api/ansible-catalog"
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "taggit",
    "django_rq",
    "drf_spectacular",
    "social_django",
    "corsheaders",
    "ansible_catalog.main",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "ansible_catalog.common.auth.middleware.KeycloakAuthMiddleware",
]

ROOT_URLCONF = "ansible_catalog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "ansible_catalog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("ANSIBLE_CATALOG_DATABASE_NAME", default="catalog"),
        "USER": env.str("ANSIBLE_CATALOG_POSTGRES_USER", default="catalog"),
        "PASSWORD": env.str(
            "ANSIBLE_CATALOG_POSTGRES_PASSWORD", default="password"
        ),
        "HOST": env.str("ANSIBLE_CATALOG_POSTGRES_HOST", default="postgres"),
        "PORT": env.str("ANSIBLE_CATALOG_POSTGRES_PORT", default="5432"),
    }
}

# REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "ansible_catalog.common.exception_handler.custom_exception_handler",
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "ansible_catalog.common.auth.keycloak_oidc.KeycloakOpenIdConnect",
    "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/ui/"
STATICFILES_DIRS = [
    BASE_DIR / "ui",
]
LOGIN_REDIRECT_URL = "/ui/index.html"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Controller Info
CONTROLLER_URL = env.str(
    "ANSIBLE_CATALOG_CONTROLLER_URL", default="https://Your_Controller_URL"
)
CONTROLLER_TOKEN = env.str(
    "ANSIBLE_CATALOG_CONTROLLER_TOKEN", default="Secret Token"
)
CONTROLLER_VERIFY_SSL = env.str(
    "ANSIBLE_CATALOG_CONTROLLER_VERIFY_SSL", default="True"
)

# Media (Icons) configuration
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Logging configuration
LOG_ROOT = env.str("CATALOG_LOG_ROOT", default="/var/log/ansible_catalog/")
LOG_FILE = "ansible_catalog.log"
MAX_BYTES = 10 * 1024 * 1024
BACKUP_COUNT = 5


if "pytest" in sys.modules:
    LOG_ROOT = env.str("CATALOG_LOG_ROOT", default="/tmp/ansible_catalog/")
    MEDIA_ROOT = os.path.join(BASE_DIR, "main/catalog/tests/data/")
    Path(LOG_ROOT).mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "%(asctime)s — %(name)s — %(levelname)s — %(message)s",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, LOG_FILE),
            "formatter": "simple",
        },
        "approval": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, LOG_FILE),
            "maxBytes": MAX_BYTES,
            "backupCount": BACKUP_COUNT,
            "formatter": "simple",
        },
        "inventory": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, LOG_FILE),
            "maxBytes": MAX_BYTES,
            "backupCount": BACKUP_COUNT,
            "formatter": "simple",
        },
        "catalog": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, LOG_FILE),
            "maxBytes": MAX_BYTES,
            "backupCount": BACKUP_COUNT,
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
        "approval": {
            "handlers": ["console", "approval"],
            "level": "INFO",
            "propagate": False,
        },
        "catalog": {
            "handlers": ["console", "catalog"],
            "level": "INFO",
            "propagate": False,
        },
        "inventory": {
            "handlers": ["console", "inventory"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

LOGIN_URL = "/login/keycloak/"

# Django Redis Queue Information
RQ_QUEUES = {
    "default": {
        "HOST": env.str("ANSIBLE_CATALOG_REDIS_HOST", default="localhost"),
        "PORT": env.int("ANSIBLE_CATALOG_REDIS_PORT", default=6379),
        "DB": env.int("ANSIBLE_CATALOG_REDIS_DB", default=0),
        "DEFAULT_TIMEOUT": 360,
    },
}

# Auto generation of openapi spec using Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Catalog API",
    "DESCRIPTION": "A set of APIs to create and manage Ansible catalogs and order from them.",
    "VERSION": "0.1.0",
    "CONTACT": {
        "email": "support@redhat.com",
    },
    "LICENSE": {
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "SERVERS": [
        {
            "url": "http://localhost:{port}/{basePath}",
            "description": "Development Server",
            "variables": {
                "port": {
                    "default": "8000",
                },
                "basePath": {
                    "default": "",
                },
            },
        },
    ],
    "COMPONENT_SPLIT_REQUEST": True,
}

SOCIAL_AUTH_JSONFIELD_ENABLED = True

KEYCLOAK_URL = env.str(
    "ANSIBLE_CATALOG_KEYCLOAK_URL", default="http://localhost:8080/auth"
).rstrip("/")
KEYCLOAK_REALM = env.str("ANSIBLE_CATALOG_KEYCLOAK_REALM", default="aap")
KEYCLOAK_CLIENT_ID = env.str(
    "ANSIBLE_CATALOG_KEYCLOAK_CLIENT_ID", default="catalog"
)
KEYCLOAK_CLIENT_SECRET = env.str(
    "ANSIBLE_CATALOG_KEYCLOAK_CLIENT_SECRET", default=""
)

SOCIAL_AUTH_KEYCLOAK_OIDC_KEY = KEYCLOAK_CLIENT_ID
SOCIAL_AUTH_KEYCLOAK_OIDC_API_URL = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
SOCIAL_AUTH_KEYCLOAK_OIDC_SECRET = KEYCLOAK_CLIENT_SECRET

# CORS
# Comma separated values list of :"SCHEME+HOST+[PORT]"
# e.g.: ANSIBLE_CATALOG_UI_ALLOWED_ORIGINS="https://example.com,catalog.example.com"
CORS_ALLOWED_ORIGINS = env.list(
    "ANSIBLE_CATALOG_UI_ALLOWED_ORIGINS", default=[]
)
CORS_ALLOW_CREDENTIALS = True
