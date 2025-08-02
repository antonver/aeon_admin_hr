# Многоэтапная сборка для оптимизации размера
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

# Основной образ
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка Python зависимостей
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование бэкенда
COPY backend/ ./backend/

# Копирование собранного фронтенда
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Копирование статических файлов
COPY backend/static ./backend/static

# Установка переменных окружения
ENV PYTHONPATH=/app
ENV PORT=8000

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "python backend/init_heroku_db.py && python backend/seed_test_data.py && uvicorn backend.main:app --host 0.0.0.0 --port $PORT"] 