#!/bin/bash

echo "🔄 Обновление фронтенда..."

# Переходим в папку frontend
cd frontend

# Устанавливаем зависимости (если нужно)
echo "📦 Проверка зависимостей..."
npm install

# Собираем фронтенд
echo "🔨 Сборка фронтенда..."
npm run build

# Очищаем папку static и копируем новые файлы
echo "📁 Копирование файлов..."
rm -rf ../backend/static
mkdir ../backend/static
cp -r build/* ../backend/static/

# Перемещаем файлы из static/static/ в static/
echo "🔄 Исправление структуры файлов..."
if [ -d "../backend/static/static" ]; then
    mv ../backend/static/static/* ../backend/static/
    rmdir ../backend/static/static
fi

# Проверяем, что файлы на месте
echo "✅ Проверка файлов..."
if [ -f "../backend/static/index.html" ]; then
    echo "   ✅ index.html найден"
else
    echo "   ❌ index.html не найден"
fi

if [ -f "../backend/static/static/js/main.*.js" ]; then
    echo "   ✅ JS файлы найдены"
else
    echo "   ❌ JS файлы не найдены"
fi

echo "✅ Фронтенд обновлен!"
echo "🌐 Приложение доступно по адресу: http://localhost:8001" 