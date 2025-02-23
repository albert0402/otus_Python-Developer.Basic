import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Загрузка переменных окружения из файла .env
load_dotenv()

# Соглашения для именования ограничений в базе данных
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Получение переменных окружения с значениями по умолчанию
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")
DB_HOST = os.getenv("DB_HOST", "pg")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "blog")

# URL-кодирование пароля (если он содержит специальные символы)
encoded_password = quote_plus(DB_PASSWORD)

# Формирование строки подключения к базе данных
db_url = f"postgresql+asyncpg://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Включение/отключение логирования SQL-запросов
db_echo = os.getenv("DB_ECHO", "False").lower() in ["true", "1"]