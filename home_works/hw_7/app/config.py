import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL", "postgresql+asyncpg://postgres:password@db:5432/postgres")
db_echo = os.getenv("DB_ECHO", "False").lower() in ("true", "1")

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}