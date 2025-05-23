"""
Django settings for config project.

Настройки используют переменные окружения из .env файла.
Все чувствительные данные должны храниться в переменных окружения.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# ======================
# Базовые настройки
# ======================

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Базовый директорий проекта (содержит manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django (критически важный для безопасности!)
# В production должен быть уникальным и храниться только в env-переменных
SECRET_KEY = os.getenv("SECRET_KEY")

# Режим отладки - ВКЛЮЧАТЬ ТОЛЬКО ДЛЯ РАЗРАБОТКИ!
# В production должно быть False
DEBUG = os.getenv("DEBUG", "False") == "True"

# Список разрешенных хостов (доменов), которые могут обслуживать проект
# Для production обязательно указать реальные домены
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,web").split(",")
]

# Доверенные источники для CSRF защиты
# Особенно важно для работы через HTTPS
CSRF_TRUSTED_ORIGINS = [
    host for host in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if host
]

# Настройка заголовков безопасности при работе за reverse proxy (nginx)
if os.getenv("USE_HTTPS", "False") == "True":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ======================
# Настройки приложений
# ======================

INSTALLED_APPS = [
    # Пользовательские приложения
    "store_app.apps.StoreAppConfig",
    # Стандартные приложения Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Сторонние приложения
    "django_celery_results",  # Для хранения результатов Celery в БД
    "health_check",  # Проверка здоровья сервисов
]

# ======================
# Промежуточное ПО (Middleware)
# ======================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ======================
# Настройки URL и шаблонов
# ======================

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # Автоматический поиск шаблонов в папках templates приложений
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ======================
# Настройки базы данных (PostgreSQL)
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "store_db"),
        "USER": os.getenv("POSTGRES_USER", "store_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "store_password"),
        "HOST": os.getenv(
            "POSTGRES_HOST", "db"
        ),  # Использует сервис 'db' из docker-compose
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# ======================
# Валидация паролей
# ======================

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

# ======================
# Локализация и время
# ======================

LANGUAGE_CODE = "ru-ru"  # Русская локализация
TIME_ZONE = "UTC"  # Временная зона по умолчанию
USE_I18N = True  # Включение интернационализации
USE_L10N = True  # Локализация форматов
USE_TZ = True  # Использование временных зон

# ======================
# Статические и медиа файлы
# ======================

# URL префикс для статических файлов
STATIC_URL = "/static/"

# Директория для сбора статических файлов командой collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"

# Дополнительные директории со статическими файлами
STATICFILES_DIRS = [
    BASE_DIR / "store_app/static",
]

# URL префикс для медиа файлов
MEDIA_URL = "/media/"

# Директория для загружаемых пользователем файлов
MEDIA_ROOT = BASE_DIR / "mediafiles"

# Тип автоматических первичных ключей
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================
# Настройки Celery
# ======================

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "redis://redis:6379/0"
)  # Брокер сообщений
CELERY_RESULT_BACKEND = "django-db"  # Хранение результатов в БД Django
CELERY_TASK_IGNORE_RESULT = False  # Сохранять результаты выполнения задач

# ======================
# Настройки email
# ======================

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.ru")  # SMTP сервер
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))  # Порт SMTP
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"  # Использовать TLS
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # Логин от почты
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Пароль от почты
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL", EMAIL_HOST_USER
)  # Email отправителя
