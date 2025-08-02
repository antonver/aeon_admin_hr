#!/bin/bash

echo "🚀 Создание нового Blueprint для исправления деплоя"
echo "=================================================="

# Проверяем авторизацию
echo "🔐 Проверяем авторизацию..."
if ! render whoami > /dev/null 2>&1; then
    echo "❌ Не авторизованы в Render. Выполните: render login"
    exit 1
fi

echo "✅ Авторизованы в Render"

# Проверяем готовность проекта
echo "🔍 Проверяем готовность проекта..."
python3 check-render-readiness.py

if [ $? -ne 0 ]; then
    echo "❌ Проект не готов к деплою"
    exit 1
fi

echo "✅ Проект готов к деплою"

# Пушим последние изменения
echo "📤 Пушим изменения в GitHub..."
git add .
git commit -m "Исправление неудачного деплоя - подготовка нового Blueprint"
git push origin main

echo "✅ Код обновлен в GitHub!"

echo ""
echo "🎯 РЕШЕНИЕ: Создать новый Blueprint"
echo ""
echo "📝 Выполните следующие шаги:"
echo ""
echo "1. Удалите старый сервис (опционально):"
echo "   - Откройте: https://dashboard.render.com/web/srv-d272anh5pdvs73c1hdpg"
echo "   - Перейдите в 'Settings' → 'Delete Service'"
echo ""
echo "2. Создайте новый Blueprint:"
echo "   - Откройте: https://dashboard.render.com"
echo "   - Нажмите 'New +' → 'Blueprint'"
echo "   - Подключите репозиторий: https://github.com/antonver/aeon_admin_hr.git"
echo "   - Выберите файл: render-fixed.yaml"
echo "   - Нажмите 'Apply'"
echo ""
echo "3. Настройте переменные окружения:"
echo "   - BOT_TOKEN (обязательно)"
echo "   - NOTION_TOKEN (опционально)"
echo "   - NOTION_DATABASE_ID (опционально)"
echo ""
echo "4. Дождитесь завершения деплоя"
echo ""
echo "🌐 Или откройте dashboard прямо сейчас:"
echo "https://dashboard.render.com"

echo ""
echo "📊 После создания нового Blueprint:"
echo "- Новый backend: https://hr-admin-backend-new.onrender.com"
echo "- Новый frontend: https://hr-admin-frontend-new.onrender.com"
echo "- Проверьте статус: ./check-deploy-status.sh" 