#!/bin/bash

echo "🔄 Принудительное обновление фронтенда на Render..."

# Проверяем что мы в корневой директории проекта
if [ ! -f "render.yaml" ]; then
    echo "❌ Ошибка: запустите скрипт из корневой директории проекта"
    exit 1
fi

# Очищаем кэш npm
echo "🧹 Очищаем кэш npm..."
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json

# Переустанавливаем зависимости
echo "📦 Переустанавливаем зависимости..."
npm install

# Собираем фронтенд заново
echo "🏗️  Пересобираем фронтенд..."
npm run build

# Возвращаемся в корень
cd ..

# Очищаем старые статические файлы
echo "🧹 Очищаем старые статические файлы..."
rm -rf backend/static/*

# Копируем новые файлы
echo "📋 Копируем новые статические файлы..."
cp -r frontend/build/* backend/static/

# Исправляем структуру папок если нужно
if [ -d "backend/static/static" ]; then
    echo "🔧 Исправляем структуру папок..."
    mv backend/static/static/* backend/static/
    rmdir backend/static/static
    echo "✅ Структура папок исправлена"
fi

# Проверяем что файлы на месте
echo "🔍 Проверяем структуру файлов:"
ls -la backend/static/
ls -la backend/static/js/ 2>/dev/null || echo "⚠️  JS файлы не найдены"
ls -la backend/static/css/ 2>/dev/null || echo "⚠️  CSS файлы не найдены"

# Создаем файл с временной меткой для принудительного обновления
echo "📝 Создаем временную метку для принудительного обновления..."
echo "Last updated: $(date)" > backend/static/.last-update
echo "Build timestamp: $(date +%s)" >> backend/static/.last-update

# Коммитим изменения
echo "💾 Коммитим изменения..."
git add .
git commit -m "Force update frontend - $(date)"

# Пушим изменения
echo "🚀 Пушим изменения на GitHub..."
git push origin main

echo "✅ Фронтенд принудительно обновлён!"
echo "📋 Следующие шаги:"
echo "1. Дождитесь завершения деплоя на Render (обычно 2-3 минуты)"
echo "2. Очистите кэш браузера (Ctrl+Shift+R или Cmd+Shift+R)"
echo "3. Проверьте обновление на сайте"

# Проверяем статус деплоя через CLI если установлен
if command -v render &> /dev/null; then
    echo "🔍 Проверяем статус деплоя..."
    render services
else
    echo "💡 Для автоматической проверки установите Render CLI:"
    echo "   curl -s https://api.render.com/downloads/cli/linux | bash"
fi 