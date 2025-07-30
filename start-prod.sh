#!/bin/bash

echo "🚀 Запуск HR Admin Panel в продакшене..."

# Проверяем наличие Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Создайте его на основе env.example"
    exit 1
fi

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose -f docker-compose.prod.yml down

# Собираем и запускаем контейнеры
echo "🔨 Собираем и запускаем контейнеры..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "✅ Приложение запущено в продакшене!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Nginx: http://localhost:80" 