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

# Исправляем структуру папок - перемещаем файлы из static/static/ в static/
if [ -d "backend/static/static" ]; then
    echo "🔧 Исправляем структуру папок..."
    mv backend/static/static/* backend/static/
    rmdir backend/static/static
    echo "✅ Структура папок исправлена"
fi

echo "✅ Статические файлы обновлены!"
echo "📝 Файлы в правильных директориях:"
ls -la backend/static/js/ 2>/dev/null && echo "✅ JS файлы в backend/static/js/" || echo "❌ JS файлы не найдены"
ls -la backend/static/css/ 2>/dev/null && echo "✅ CSS файлы в backend/static/css/" || echo "❌ CSS файлы не найдены"

echo "🚀 Готово к деплою на Render!" 