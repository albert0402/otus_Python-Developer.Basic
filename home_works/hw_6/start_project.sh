#!/bin/bash

# Запускает контейнер PostgreSQL в фоновом режиме с использованием Docker Compose
echo "Запуск контейнера PostgreSQL..."
docker compose up -d pg

# Активирует виртуальное окружение Python
echo "Активируем виртуальное окружение..."
source ./.venv/bin/activate

# Устанавливает все зависимости, указанные в файле requirements.txt
echo "Установка зависимостей..."
pip install -r requirements.txt

# Инициализирует директорию alembic для управления миграциями (если еще не инициализирована)
if [ ! -d "alembic" ]; then
    echo "Инициализация Alembic..."
    alembic init alembic
fi

# Проверка наличия миграций и создание первой миграции, если она отсутствует
if [ ! -f "alembic/versions/initial_migration.py" ]; then
    echo "Создание первой миграции..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Применение миграций к базе данных
echo "Применение миграций к базе данных..."
alembic upgrade head

# Запуск приложения (замените 'app.py' на имя вашего файла приложения)
echo "Запуск приложения..."
python main.py

echo "Проект успешно запущен!"
