# Dockerfile
# Используйте базовый образ с Python
FROM python:3.10-slim

# Установите рабочую директорию
WORKDIR /hw5

# Скопируйте файл зависимостей
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения
COPY . .

# Откройте порт 8000 для приложения
EXPOSE 8000

# Запустите сервер uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]