#!/bin/bash

echo "🔍 Проверяем статус деплоя на Render..."
echo ""

# Проверяем доступность основного URL
echo "🌐 Проверяем доступность сайта..."
if curl -s -o /dev/null -w "%{http_code}" https://hr-admin-backend.onrender.com | grep -q "200"; then
    echo "✅ Сайт доступен (HTTP 200)"
else
    echo "❌ Сайт недоступен или возвращает ошибку"
fi

echo ""

# Проверяем статические файлы
echo "📁 Проверяем статические файлы..."
JS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://hr-admin-backend.onrender.com/static/js/main.f8b9cbc8.js)
CSS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://hr-admin-backend.onrender.com/static/css/main.16434665.css)

echo "📄 JS файл: $JS_STATUS"
echo "🎨 CSS файл: $CSS_STATUS"

if [ "$JS_STATUS" = "200" ] && [ "$CSS_STATUS" = "200" ]; then
    echo "✅ Все статические файлы доступны"
else
    echo "❌ Проблемы со статическими файлами"
fi

echo ""
echo "🔗 Ссылка на сайт: https://hr-admin-backend.onrender.com"
echo "📊 Render Dashboard: https://dashboard.render.com" 