FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения
COPY . .

# Убедитесь, что gunicorn и зависимость uvicorn установлены
RUN pip install gunicorn uvicorn

# Стартовое приложение через gunicorn с uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
