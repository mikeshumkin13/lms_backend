import os
from pathlib import Path
from dotenv import load_dotenv

# Базовая директория
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения
load_dotenv(BASE_DIR / ".env")


# Настройки безопасности
SECRET_KEY = "django-insecure-n=05vn!92_m%j0^be04-%gbku%v!!lrwt(vq95$cj&zzko4l09"
DEBUG = True

print("DEBUG =", os.getenv("DEBUG"))
print("ALLOWED_HOSTS_RAW =", os.getenv("ALLOWED_HOSTS"))
import sys
print("⚠️ settings.py is being used:", __file__, file=sys.stderr)

# ALLOWED_HOSTS из .env
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]


print("⚠️ ALLOWED_HOSTS =", ALLOWED_HOSTS)
print("⚠️ repr(ALLOWED_HOSTS):", repr(ALLOWED_HOSTS))

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Celery (Redis)
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Moscow"

# Django apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "materials",
    "drf_yasg",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# БД
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

# Пароли
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Язык, время
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Статика
STATIC_URL = "static/"

# Первичный ключ
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Кастомный пользователь
AUTH_USER_MODEL = "users.User"

# DRF
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT авторизация. Пример: Bearer <твой токен>",
        }
    },
}

# Celery Beat
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "deactivate-inactive-users-every-night": {
        "task": "users.tasks.deactivate_inactive_users_task",
        "schedule": crontab(hour=0, minute=0),
    },
}


print("===== DEBUG ENVIRONMENT =====")
print("os.getenv('ALLOWED_HOSTS') =", os.getenv("ALLOWED_HOSTS"))
print("ALLOWED_HOSTS =", ALLOWED_HOSTS)


