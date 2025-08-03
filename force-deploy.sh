#!/bin/bash

echo "🚀 Принудительный деплой с обновлением фронтенда..."

# Обновляем статические файлы
./update-static.sh

# Добавляем все изменения в git
echo "📝 Добавляем изменения в git..."
git add .

# Создаем коммит с временной меткой
echo "💾 Создаем коммит..."
git commit -m "Force update: $(date '+%Y-%m-%d %H:%M:%S') - Обновление фронтенда"

# Пушим изменения
echo "📤 Пушим изменения на Render..."
git push origin main

echo "✅ Деплой запущен! Проверьте статус на Render через несколько минут."
echo "🔗 Ссылка на деплой: https://hr-admin-backend.onrender.com" 