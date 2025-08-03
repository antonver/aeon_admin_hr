#!/bin/bash

echo "🔄 Обновляем статические файлы фронтенда..."

# Переходим в директорию фронтенда
cd frontend

# Устанавливаем зависимости если нужно
if [ ! -d "node_modules" ]; then
    echo "📦 Устанавливаем зависимости..."
    npm install
fi

# Собираем фронтенд
echo "🏗️  Собираем React приложение..."
npm run build

# Возвращаемся в корневую директорию
cd ..

# Очищаем старые статические файлы
echo "🧹 Очищаем старые файлы..."
rm -rf backend/static/*

# Копируем новые файлы
echo "📋 Копируем новые статические файлы..."
cp -r frontend/build/* backend/static/

echo "✅ Статические файлы обновлены!"
echo "📝 Новые хеши файлов:"
ls -la backend/static/static/js/
ls -la backend/static/static/css/

echo "🚀 Готово к деплою на Render!" 