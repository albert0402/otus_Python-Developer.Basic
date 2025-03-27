# Django Магазин c Celery и Redis

Этот проект представляет собой магазин на Django с расширенной функциональностью (с CBV (Class-Based Views) и использованием Pytest), включая управление товарами, категориями, формами и админкой.

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