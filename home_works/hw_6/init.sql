-- Установка расширения citext
CREATE EXTENSION IF NOT EXISTS citext;

-- Создание пользователя, если он не существует
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'app') THEN
    CREATE USER app WITH PASSWORD 'apppassword';
  END IF;
END $$;

-- Создание базы данных, если она не существует
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'blog') THEN
    CREATE DATABASE blog OWNER app;
    GRANT ALL PRIVILEGES ON DATABASE blog TO app;
  END IF;
END $$;