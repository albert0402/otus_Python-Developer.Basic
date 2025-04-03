# Django Магазин 

Этот проект представляет собой магазин на Django с расширенной функциональностью с CBV (Class-Based Views) и использованием Pytest, включая управление товарами, категориями, формами и админкой.

---
# Последовательность запуска проекта через Docker


## 1. Инициализация и сборка Docker-окружения

#### Проверка состояния Docker
```bash
docker info
```

#### Сборка и запуск контейнеров
```bash
docker-compose up -d --build
```

### Дополнительные команды Docker:

#### Проверить статус контейнеров
```bash
docker-compose ps
```

#### Остановка текущих контейнеры
```bash
docker-compose down -v
```

#### Полный сброс всех контейнеров
```bash
docker-compose down --volumes --rmi local
```

#### Полная очистка Docker
Будьте осторожны - эта команда удалит ВСЕ неиспользуемые ресурсы Docker (образы, контейнеры, тома, сети) всей системы.
```bash
docker system prune -a --volumes
```


## 2. Мониторинг работы Docker контейнеров  

#### Просмотр логов работы всех контейнеров проекта
```bash
docker-compose logs -f
```

#### Просмотр логов работы контейнера проекта - web
```bash
docker-compose logs -f web
```

#### Просмотр логов работы контейнера прокси-сервера Nginx - nginx
```bash
docker-compose logs -f nginx
```

#### Просмотр логов работы контейнера брокера сообщений Redis - redis
```bash
docker-compose logs -f redis
```

#### Просмотр логов работы контейнера базы данных PostgreSQL - db
```bash
docker-compose logs -f db
```


## 3. Проверка работоспособности

#### Проверка работы веб-приложения через Nginx (внешний доступ)
```bash
curl -v http://localhost:8000
```

#### Проверить соединение между контейнерами (внутри Docker-сети)
```bash
docker-compose exec nginx curl -v http://web:8000
```

#### Проверить работу Django
```bash
docker-compose exec web curl -v http://localhost:8000
```

#### Проверка "здоровья" проекта
```bash
docker-compose exec web curl http://web:8000/health/
```

#### Проверка статики
```bash
curl -v http://localhost:8000/static/admin/css/base.css
```

## 4. Управление Django-приложением

### Миграции:

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

### Администрирование:
#### Создание суперпользователя:
```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

#### Запуск shell
```bash
docker-compose exec web poetry run python manage.py shell
```

#### Проверка работы Redis
```bash
docker-compose exec redis redis-cli ping
```

--- 

## Последовательность ручного запуска проекта 

### 1. Poetry

#### Создаем poetry в проекте
```bash
poetry init
```

#### Получение информации о настройках poetry
```bash
poetry env info
```

#### Добавление зависимостей
```bash
poetry add django  # Пример основных зависимостей
poetry add --group pytest black # Dev-зависимости 
```

#### Активация виртуального окружения poetry
```bash
poetry env activate
```

#### Проверка окружения poetry
```bash
poetry env list
```

#### Установка зависимостей poetry
```bash
poetry install
```
#### Установка зависимостей дополнительных зависимостей poetry
```bash
poetry lock
```

#### Деактивация виртуального окружения poetry происходит после закрытия терминала




####
```bash

```









---

## Запускайте сервисы Магазина в правильном порядке


ПОЛНАЯ ПЕРЕЗАГРУЗКА
# Остановите ВСЕ процессы принудительно
sudo kill -9 $(ps aux | grep -E 'redis|celery|python3' | awk '{print $2}')

# Убедитесь, что ничего не осталось
ps aux | grep -E "redis|celery|python3" | grep -v grep


### В ПЕРВОМ терминале - Redis (в virtualenv)
```bash
source .venv/bin/activate
redis-server redis.conf --daemonize yes
```

### Во ВТОРОМ терминале - Celery (тоже в virtualenv)
```bash
source .venv/bin/activate
celery -A config worker --loglevel=debug --without-heartbeat --without-mingle --concurrency=1
```

### В ТРЕТЬЕМ терминале - Django (тоже в virtualenv)
```bash
source .venv/bin/activate
python manage.py runserver
```

### В ЧЕТВЕРТОМ терминале - Django (тоже в virtualenv)
Проверка на тестовой задаче: 
```bash
source .venv/bin/activate
python manage.py shell

from config.celery import app
app.control.ping(timeout=5)  #[{'celery@MacBook-Pro-Albert.local': {'ok': 'pong'}}]

from store_app.tasks import send_category_notification
send_category_notification.delay(action="тест", category_id=1) # Успешно приходит сообщение
```

---

## 1. Звпуск Django-проекта

### Переход в директорию проекта Django
```bash
cd <project_folder>
```

### Запуск приложения Django
```bash
python manage.py startapp store_app
```


## 2. Включение Redis в проекте на MacOS

### Установка Redis (если не установлен)
```bash
brew install redis
```

### Включение Redis
```bash
brew services start redis
```

### Проверка работы Redis:
```bash
redis-cli ping  # Должно вернуть PONG
```

### Остановка работы Redis:
```bash
brew services stop redis
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