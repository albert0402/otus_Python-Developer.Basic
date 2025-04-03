# Базовый образ - Python 3.12 на slim-образе (уменьшенный размер)
FROM python:3.12-slim

# Установка системных зависимостей:
# - build-essential: компиляторы и инструменты для сборки Python-пакетов
# - libpq-dev: зависимости для работы с PostgreSQL
# - curl: для healthcheck и отладки
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*  # Очистка кеша apt для уменьшения размера образа

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка Poetry (менеджер зависимостей Python)
# Фиксируем версию для воспроизводимости сборок
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Копируем файлы зависимостей в первую очередь
# Это позволяет Docker кэшировать этот слой и не переустанавливать 
# зависимости при изменении кода, если зависимости не менялись
COPY pyproject.toml poetry.lock* ./

# Установка Python-зависимостей:
# - Отключаем создание virtualenv (используем системный Python)
# - Устанавливаем только основные зависимости (без dev-зависимостей)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Копируем весь остальной код проекта
# Делаем это после установки зависимостей для лучшего использования кэша Docker
COPY . .

# Настройка прав для статических файлов:
# - Создаем директории для статики и медиафайлов
# - Устанавливаем правильные права (владелец 1000:1000)
RUN mkdir -p /app/staticfiles /app/mediafiles && \
    chown -R 1000:1000 /app/staticfiles /app/mediafiles && \
    chmod -R 755 /app/staticfiles /app/mediafiles

# Декларация о том, что контейнер слушает порт 8000
# (фактическое пробрасывание порта делается в docker-compose.yml)
EXPOSE 8000

# Команда запуска приложения:
# - Используем poetry для запуска gunicorn
# - Gunicorn будет слушать все интерфейсы (0.0.0.0) на порту 8000
# - 3 воркера для обработки запросов
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]