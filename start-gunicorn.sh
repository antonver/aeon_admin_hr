#!/bin/bash

# Скрипт запуска Gunicorn с ASGI worker для Render
echo "🚀 Запускаем Gunicorn с ASGI worker..."

# Применяем миграции базы данных
echo "🗄️  Применяем миграции базы данных..."
cd backend
alembic upgrade head
cd ..

# Запускаем Gunicorn с ASGI worker
echo "🌐 Запускаем Gunicorn с UvicornWorker..."
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT app:application 