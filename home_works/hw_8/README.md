# Django Магазин

Этот гайд поможет вам создать проект магазина на Django, определить модели и работать с ORM.

## 1. Создание Django-проекта и приложения

### Создание нового проекта Django
```bash
django-admin startproject config .
cd config
```

### Создание нового приложения Django
```bash
python manage.py startapp store_app
```

### Добавление приложения в `settings.py`
Открыть `config/settings.py` и добавить `'store_app'` в `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'store_app',
]
```

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
- `category`: связь с категорией через `ForeignKey`.

## 3. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Работа с ORM

### Создание команды управления для заполнения базы данных
Создать структуру директорий в `storestore_app/`:
```bash
mkdir -p store_app/management/commands
```

Создать новый файл `store_app/management/commands/fill_db.py`, который заполняет базу случайными категориями и товарами.

### Запуск команды для заполнения базы
```bash
python manage.py fill_db
```

## 5. Запуск сервера
```bash
python manage.py runserver
```

Перейдите по адресу `http://127.0.0.1:8000/`, чтобы увидеть ваш Django-проект.