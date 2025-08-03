#!/bin/bash

echo "🚀 Pre-build скрипт для Render..."

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "📦 Устанавливаем Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get update
    apt-get install -y nodejs
fi

echo "📋 Версии:"
node --version
npm --version

# Собираем фронтенд
echo "🏗️  Собираем фронтенд..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Pre-build завершен!"

# Дополнительная проверка для отладки на Render
echo "🔍 Проверяем что файлы собрались:"
if [ -d "frontend/build" ]; then
    echo "✅ frontend/build существует"
    ls -la frontend/build/
    if [ -d "frontend/build/static" ]; then
        echo "✅ frontend/build/static существует"
        ls -la frontend/build/static/
    fi
else
    echo "❌ frontend/build не существует!"
fi 