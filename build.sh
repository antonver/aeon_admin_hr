#!/bin/bash

# Скрипт сборки для Render
echo "🚀 Начинаем сборку проекта..."

# Устанавливаем зависимости Python
echo "📦 Устанавливаем Python зависимости..."
pip install -r backend/requirements.txt

# Создаем необходимые директории
echo "📁 Создаем директории..."
mkdir -p backend/static

# Копируем статические файлы фронтенда в бэкенд (фронтенд уже собран в render.yaml)
echo "📋 Копируем статические файлы фронтенда..."
if [ -d "frontend/build" ]; then
    echo "🧹 Очищаем старые статические файлы..."
    rm -rf backend/static/*
    echo "📋 Копируем новые статические файлы..."
    cp -r frontend/build/* backend/static/
    echo "✅ Статические файлы обновлены"
    echo "📁 Проверяем структуру файлов:"
    ls -la backend/static/
    ls -la backend/static/static/js/ 2>/dev/null || echo "⚠️  JS файлы не найдены"
    ls -la backend/static/static/css/ 2>/dev/null || echo "⚠️  CSS файлы не найдены"
else
    echo "⚠️  Директория frontend/build не найдена"
    mkdir -p backend/static
fi

# Инициализируем базу данных
echo "🗄️  Инициализируем базу данных..."
cd backend
python init_heroku_db.py

echo "✅ Сборка завершена!" 