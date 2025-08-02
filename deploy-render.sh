#!/bin/bash

echo "🚀 Быстрый деплой на Render"
echo "=========================="

# Проверяем готовность проекта
echo "🔍 Проверяем готовность проекта..."
python3 check-render-readiness.py

if [ $? -ne 0 ]; then
    echo "❌ Проект не готов к деплою"
    exit 1
fi

# Пушим изменения в GitHub
echo "📤 Пушим изменения в GitHub..."
git add .
git commit -m "Обновление для деплоя $(date)"
git push origin main

echo ""
echo "✅ Код обновлен в GitHub!"
echo ""
echo "📝 Следующие шаги для деплоя на Render:"
echo "1. Зайдите на https://render.com"
echo "2. Создайте аккаунт (если еще нет)"
echo "3. Нажмите 'New +' → 'Blueprint'"
echo "4. Подключите репозиторий: https://github.com/antonver/aeon_admin_hr.git"
echo "5. Выберите файл render.yaml"
echo "6. Нажмите 'Apply'"
echo ""
echo "🔧 После создания сервисов настройте переменные окружения:"
echo "- BOT_TOKEN (обязательно)"
echo "- NOTION_TOKEN (опционально)"
echo "- NOTION_DATABASE_ID (опционально)"
echo ""
echo "📖 Подробные инструкции: RENDER_DEPLOYMENT.md"
echo "⚡ Быстрый старт: QUICK_RENDER_DEPLOY.md" 