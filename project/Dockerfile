FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя и группы celery
RUN groupadd -r celery && \
    useradd -r -g celery celery && \
    mkdir -p /home/celery && \
    chown celery:celery /home/celery

# Обновление pip и установка poetry
RUN pip install --upgrade pip && pip install poetry

# Рабочая директория
WORKDIR /app

# Копирование и установка зависимостей
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

# Копирование остальных файлов
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/staticfiles /app/mediafiles && \
    chown -R celery:celery /app/staticfiles /app/mediafiles

# Разрешения для пользователя celery
RUN chmod -R 755 /app/staticfiles /app/mediafiles

EXPOSE 8000

# Рекомендуется указать USER, если приложение не требует root
USER celery