# FastAPI Blog Project

## Описание
Этот проект представляет собой веб-приложение на FastAPI для работы с пользователями и постами. Оно использует PostgreSQL в качестве базы данных и работает в продакшн-режиме с Gunicorn и Uvicorn.

## Требования
- Docker и Docker Compose
- Python 3.9+
- Poetry (для управления зависимостями)

## Установка и запуск

1. **Клонировать репозиторий:**
   ```sh
   git clone https://github.com/<adress>.git
   cd <fastapi-project-folder>
   ```

2. **Запустить контейнеры:**
   ```sh
   docker-compose down                                   
   docker-compose build --no-cache
   docker-compose up -d
   ```
   Это создаст и запустит контейнеры для FastAPI-приложения и базы данных PostgreSQL.

3. **Проверить, что внутри контейнеров все корректно работает:**
   ```sh
   docker-compose logs -f
   ```
   Пойдут логи из всех контейнеров в терминале.

4. **Доступ к API:**
   - Открыть в браузере [http://localhost:8000/docs](http://localhost:8000/docs) для документации Swagger.
   - Также доступны страницы [http://127.0.0.1:8000/posts](http://127.0.0.1:8000/posts) и [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)

5. **Остановка контейнеров:**
   ```sh
   docker-compose down
   ```

## Работа с миграциями Alembic
Alembic используется для управления схемой базы данных.

1. **Создать новую миграцию:**
   ```sh
   alembic revision --autogenerate -m "initial migration"
   ```

2. **Применить миграции:**
   ```sh
   alembic upgrade head
   ```

3. **Откатиться к предыдущей версии:**
   ```sh
   alembic downgrade -1
   ```

4. **Откатить все миграции до начального состояния:**
   ```sh
   alembic downgrade base
   ```

5. **Проверить текущую версию миграции:**
   ```sh
   alembic current
   ```

## Парсинг данных
Для получения данных о пользователях и постах используется файл `app/jsonplaceholder_requests.py`. Он загружает данные с `https://jsonplaceholder.typicode.com/` и записывает их в базу данных.

При старте FastAPI данные загружаются автоматически.
Если нужно запустить загрузку вручную:
```sh
poetry run python app/services/data_loader.py
```

## Полезные команды

### **Перезапуск приложения**
```sh
docker-compose restart
```

### **Открыть доступ к базе данных из контейнера**
```sh
docker-compose exec db psql -U postgres -d fastapi_db
```

### **Форматирование кода**
```sh
black .
```