FROM python:3.12-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --upgrade pip && pip install poetry

# Рабочая директория
WORKDIR /app

# Сначала копируем только зависимости
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей проекта
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

# Затем копируем остальной код
COPY . .

# Создание директорий для статики
RUN mkdir -p /app/staticfiles /app/mediafiles

# Порт для Django
EXPOSE 8000