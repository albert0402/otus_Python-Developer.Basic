# Django Магазин 

Этот проект представляет собой магазин на Django с расширенной функциональностью с CBV (Class-Based Views) и использованием Pytest, включая управление товарами, категориями, формами и админкой.


---

## Быстрый старт проекта

#### Проверка состояния Docker:
```bash
docker info
```

#### Сборка и запуск контейнеров:
```bash
docker-compose up -d --build
```

#### Загрузка категорий в интернет магазин:
```bash
docker-compose exec web poetry run python manage.py loaddata store_app/fixtures/categories.json
```

#### Загрузка товаров в интернет магазин:
```bash
docker-compose exec web poetry run python manage.py loaddata store_app/fixtures/products.json
```

---

## Полная последовательность запуска проекта через Docker


### 1. Инициализация и сборка Docker-окружения

#### Проверка состояния Docker:
```bash
docker info
```

#### Сборка и запуск контейнеров:
```bash
docker-compose up -d --build
```

### 1.1 Дополнительные команды Docker:

#### Проверить статус контейнеров:
```bash
docker-compose ps
```

#### Остановка текущих контейнеры:
```bash
docker-compose down -v
```

#### Полный сброс всех контейнеров:
```bash
docker-compose down --volumes --rmi local
```

#### Полная очистка Docker:
Будьте осторожны - эта команда удалит ВСЕ неиспользуемые ресурсы Docker (образы, контейнеры, тома, сети) всей системы.
```bash
docker system prune -a --volumes
```


### 2. Мониторинг работы Docker контейнеров  

#### Просмотр логов работы всех контейнеров проекта:
```bash
docker-compose logs -f
```

#### Просмотр логов работы контейнера проекта - web:
```bash
docker-compose logs -f web
```

#### Просмотр логов работы контейнера прокси-сервера Nginx - nginx:
```bash
docker-compose logs -f nginx
```

#### Просмотр логов работы контейнера брокера сообщений Redis - redis:
```bash
docker-compose logs -f redis
```

#### Просмотр логов работы контейнера базы данных PostgreSQL - db:
```bash
docker-compose logs -f db
```


### 3. Проверка работоспособности

#### Проверка работы веб-приложения через Nginx (внешний доступ):
```bash
curl -v http://localhost:8000
```

#### Проверить соединение между контейнерами (внутри Docker-сети):
```bash
docker-compose exec nginx curl -v http://web:8000
```

#### Проверить работу Django:
```bash
docker-compose exec web curl -v http://localhost:8000
```

#### Проверка "здоровья" проекта:
```bash
docker-compose exec web curl http://web:8000/health/
```

#### Проверка статики:
```bash
curl -v http://localhost:8000/static/admin/css/base.css
```

### 4. Управление Django-приложением

#### Автоматическое форматирование проекта к стандарту PEP-8:
```bash
poetry run black .
```

### 4.1 Миграции

#### Создание миграций (после изменения моделей):
```bash
docker-compose exec web poetry run python manage.py makemigrations
```

#### Применение миграций к базе данных:
```bash
docker-compose exec web poetry run python manage.py migrate
```

#### Проверка статуса миграций:
```bash
docker-compose exec web poetry run python manage.py showmigrations
```

### 4.2 Администрирование

#### Создание суперпользователя:
```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

#### Запуск shell:
```bash
docker-compose exec web poetry run python manage.py shell
```

#### Проверка работы Redis:
```bash
docker-compose exec redis redis-cli ping
```


### 5. Работа с базой данных Django-приложения

База данных интернет магазина хранится в директории /store_app/fixtures в формате .json.
Она состоит из двух файлов:
- файл categories.json используется для хранения категорий в магазине;
- файл products.json используется для хранения товаров в магазине.

#### Загрузка категорий в интернет магазин:
```bash
docker-compose exec web poetry run python manage.py loaddata store_app/fixtures/categories.json
```

#### Выгрузка данных из класса Category с правильными отступами --indent 4:
```bash
docker-compose exec web poetry run python manage.py dumpdata store_app.Category --indent 4 > store_app/fixtures/categories.json
```

#### Загрузка товаров в интернет магазин:
```bash
docker-compose exec web poetry run python manage.py loaddata store_app/fixtures/products.json
```

#### Выгрузка данных из класса Product с правильными отступами --indent 4:
```bash
docker-compose exec web poetry run python manage.py dumpdata store_app.Product --indent 4 > store_app/fixtures/products.json
```


## 6. Управление Django-приложением через Makefile

#### Список всех доступных команд Django-приложения:
```bash
make help
```

### 6.1 Docker Utilities (Управление контейнерами)

#### Просмотр логов всех сервисов в реальном времени:
```bash
make logs
```

#### Запуск контейнеров в фоновом режиме:
```bash
make up
```

#### Остановка и удаление контейнеров:
```bash
make down
```

#### Пересборка и перезапуск контейнеров:
```bash
make rebuild
```

### 6.2 Django Management (Управление Django)

#### Применить миграции базы данных:
```bash
make migrate
```

#### Создать новые миграции после изменения моделей:
```bash
make makemigrations
```

#### Показать статус всех миграций:
```bash
make showmigrations
```

#### Создать суперпользователя Django:
```bash
make createsuperuser
```

#### Запустить Django shell:
```bash
make shell
```

#### Запустить тесты:
```bash
make test
```

#### Собрать статические файлы:
```bash
make collectstatic
```

####  Подключиться к PostgreSQL через psql:
```bash
make db-shell
```

#### Работа с Redis:
```bash
make redis-ping
```


---

## Полная последовательность ручного запуска проекта

### 1. Настройка Poetry и виртуального окружения

#### Инициализация проекта (если ещё нет файла pyproject.toml):
```bash
poetry init
```

#### Добавление подзависимостей для воспроизводимости окружения(если ещё нет файла poetry.lock):
```bash
poetry lock
```
Нужно использовать:
- после изменения pyproject.toml (добавили или удалили зависимости, изменили версионные ограничения);
- для обновления зависимостей.


#### Добавление основных зависимостей:
```bash
poetry add django gunicorn psycopg2-binary redis celery
```

#### Добавление dev-зависимостей:
```bash
poetry add --group dev pytest black isort flake8
```

#### Активация виртуального окружения:
```bash
poetry shell  # Автоматически активирует окружение
```

#### Установка всех зависимостей:
```bash
poetry install
```

#### Проверка окружения:
```bash
poetry env info
```


### 2. Настройка и запуск сервисов

#### Запуск PostgreSQL (если не установлен):
```bash
brew install postgresql
brew services start postgresql
```

#### Создание БД (если не создана):
```bash
createdb store_db -U store_user
```

#### Настройка Redis:
```bash
brew install redis
brew services start redis
```

#### Проверка Redis:
```bash
redis-cli ping  # Должен вернуть PONG
```


### 3. Запуск проекта (в разных терминалах)

#### Терминал 1 - Redis:
```bash
poetry shell
redis-server
```

#### Терминал 2 - Celery:
```bash
poetry shell
celery -A config worker --loglevel=info
```

#### Терминал 3 - Django сервер:
```bash
poetry shell
python manage.py migrate
python manage.py runserver
```

#### Терминал 4 - Gunicorn (для production-режима):
```bash
poetry shell
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```


### 4. Управление проектом

#### Применение миграций:
```bash
poetry run python manage.py migrate
```

#### Создание суперпользователя:
```bash
poetry run python manage.py createsuperuser
```

#### Запуск тестов:
```bash
poetry run pytest
```

#### Сбор статики:
```bash
poetry run python manage.py collectstatic
```


### 5. Остановка сервисов

#### Остановка всех сервисов
Остановка Django и Celery:
```bash
pkill -f "python manage.py runserver"
pkill -f "celery worker"
```
Остановка Redis и PostgreSQL:
```bash
brew services stop redis
brew services stop postgresql
```

#### Проверка работающих процессов:
```bash
ps aux | grep -E "python|celery|redis|postgres"
```

#### Удаление виртуального окружения
```bash
poetry env remove python
```

#### Остановка всех сервисов
```bash
brew services stop --all
```

4. Для проверки работоспособности Celery:
```bash
poetry run python manage.py shell
>>> from config.celery import app
>>> app.control.ping()  # Должен вернуть pong
```

---

## 2. Определение моделей

### Модель категорий (Category)
Файл: `store_app/models.py`
- `name`: название категории (уникальное).
- `description`: описание категории.

### Модель товаров (Product)
Файл: `store_app/models.py`
- `name`: название товара.
- `description`: описание товара.
- `price`: цена товара.
- `created_at`: дата создания товара (автоматически заполняется).
- `categories`: связь с категориями через `ManyToManyField`.
- `is_available`: статус доступности товара.

---

## 3. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4. Работа с ORM

### Запуск команды для заполнения базы из файла `data_fixture.json`
```bash
python manage.py loaddata store_app/fixtures/data_fixture.json
```

### Запуск команды для выгрузки данных из базы в файл `dumped_data.json`
```bash
python manage.py dumpdata store_app --indent 4 > store_app/fixtures/dumped_data.json
```

---

## 5. Создание шаблонов

### Базовый шаблон (`base.html`)
- Используется для наследования всеми остальными шаблонами.
- Содержит блоки `title` и `content`.

### Меню (`menu.html`)
- Навигационное меню для перехода между страницами.
- Включает ссылки на главную страницу, список товаров, список категорий и страницу "О нас".

### Главная страница (`main_page.html`)
- Приветственное сообщение и инструкции.
- Используется как домашняя страница по адресу `/`.

### Список товаров (`product_list.html`)
- Отображает список товаров с названием, описанием, ценой и доступностью.
- Поддерживает фильтрацию по категории, цене и доступности.
- Содержит кнопки для добавления, редактирования и удаления товаров.

### Детали товара (`product_detail.html`)
- Отображает все данные о товаре, включая категории и статус доступности.
- Содержит кнопки для редактирования товара и возврата к списку товаров.

### Форма добавления и редактирования товара (`product_form.html`)
- Универсальный шаблон формы товара.
- Валидирует введенные данные и отображает ошибки.

### Список категорий (`category_list.html`)
- Отображает список категорий с названием и описанием.
- Содержит кнопки для добавления и редактирования категорий.

### Форма добавления и редактирования категории (`category_form.html`)
- Универсальный шаблон формы категории.
- Валидирует введенные данные и отображает ошибки.

---

## 6. Создание форм

### Форма товара (`ProductModelForm`)
- Работает с моделью `Product`.
- Поля: `name`, `description`, `price`, `categories`, `is_available`.
- Валидация:
  - Цена не может быть отрицательной.
  - Название не менее 3 символов.

### Форма категории (`CategoryModelForm`)
- Работает с моделью `Category`.
- Поля: `name`, `description`.
- Валидация:
  - Название не менее 3 символов.

---

## 7. Настройка админки

### Кастомизация модели `Product`
- `list_display`: `name`, `price`, `get_categories`, `is_available`.
- `ordering`: По названию и цене.
- `search_fields`: Поиск по названию и описанию.
- `readonly_fields`: Поле `created_at`.
- Кастомные действия:
  - **Add new product**: Добавляет товар с категорией по умолчанию.
  - **Update product details**: Обновляет поля товаров.
  - **Set price to 500**: Устанавливает цену.
  - **Mark as out of stock**: Делает товары недоступными.

### Кастомизация модели `Category`
- `list_display`: `name`, `description`.
- `ordering`: По названию.
- `search_fields`: Поиск по названию и описанию.
- Кастомные действия:
  - **Add new category**: Добавляет новую категорию.

---

## 8. Запуск сервера
```bash
python manage.py runserver
```

Перейдите по адресу `http://127.0.0.1:8000/`, чтобы увидеть ваш Django-проект.

---

## 9. Основные маршруты

- **Главная страница**: `http://127.0.0.1:8000/`
- **Список товаров**: `http://127.0.0.1:8000/products/`
- **Детали товара**: `http://127.0.0.1:8000/products/<product_id>/`
- **Добавление товара**: `http://127.0.0.1:8000/products/add/`
- **Редактирование товара**: `http://127.0.0.1:8000/products/edit/<product_id>/`
- **Удаление товара**: `http://127.0.0.1:8000/products/delete/<product_id>/`
- **Список категорий**: `http://127.0.0.1:8000/categories/`
- **Добавление категории**: `http://127.0.0.1:8000/categories/add/`
- **Редактирование категории**: `http://127.0.0.1:8000/categories/edit/<category_id>/`
- **О нас**: `http://127.0.0.1:8000/about/`

---

## 10. Примеры использования

### Добавление товара
1. Перейдите на страницу `http://127.0.0.1:8000/products/add/`.
2. Заполните форму и нажмите "Сохранить".

### Редактирование товара
1. Перейдите на страницу `http://127.0.0.1:8000/products/<id>/`.
2. Нажмите кнопку "Редактировать", внесите изменения и сохраните.

### Удаление товара
1. На странице списка товаров нажмите "Удалить".
2. Подтвердите удаление на следующей странице.

### Добавление/редактирование категорий
1. Используйте соответствующие ссылки на странице списка категорий.

---

## 11. Зависимости

- Django 4.2+
- Python 3.8+
- Pytest для тестирования