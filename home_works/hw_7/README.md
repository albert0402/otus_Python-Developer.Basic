# FastAPI Blog Project

## Описание
Этот проект представляет собой веб-приложение на FastAPI для работы с пользователями и постами. Оно использует PostgreSQL в качестве базы данных и работает в продакшн-режиме с Gunicorn и Uvicorn.

## Требования
- Docker и Docker Compose

## Установка и запуск

1. **Клонировать репозиторий:**
   ```sh
   git clone https://github.com/<adress>.git
   cd <fastapi-project-folder>
   ```

2. **Создать `.env` файл (при необходимости)**
   ```sh
   cp .env.example .env
   ```

3. **Запустить контейнеры:**
   ```sh
   docker-compose up --build
   ```
   Это создаст и запустит контейнеры для FastAPI-приложения и базы данных PostgreSQL.

4. **Доступ к API:**
   - Открыть в браузере [http://localhost:8000/docs](http://localhost:8000/docs) для документации Swagger.

5. **Остановка контейнеров:**
   ```sh
   docker-compose down
   ```

## Парсинг данных
Для получения данных о пользователях и постах используется файл `app/jsonplaceholder_requests.py`. Он загружает данные с `https://jsonplaceholder.typicode.com/` и записывает их в базу данных.

## База данных
По умолчанию используется PostgreSQL. Подключение настраивается через `DATABASE_URL` в `.env`.