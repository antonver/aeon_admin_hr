#!/bin/bash

echo "🚀 Запуск деплоя"
echo "================"

# Проверяем авторизацию
echo "🔐 Проверяем авторизацию..."
if ! render whoami > /dev/null 2>&1; then
    echo "❌ Не авторизованы в Render. Выполните: render login"
    exit 1
fi

echo "✅ Авторизованы в Render"

# Получаем информацию о сервисе
echo "🔍 Получаем информацию о сервисе..."
SERVICE_INFO=$(render services --output json | jq -r '.[] | select(.service.name == "aeon_admin_hr")')

if [ -z "$SERVICE_INFO" ]; then
    echo "❌ Сервис aeon_admin_hr не найден"
    exit 1
fi

SERVICE_ID=$(echo "$SERVICE_INFO" | jq -r '.service.id')
SERVICE_URL=$(echo "$SERVICE_INFO" | jq -r '.service.dashboardUrl')

echo "✅ Найден сервис: aeon_admin_hr (ID: $SERVICE_ID)"

# Проверяем, что app.py существует
if [ ! -f "app.py" ]; then
    echo "❌ app.py не найден. Запустите сначала: ./fix-and-deploy.sh"
    exit 1
fi

echo "✅ app.py найден"

# Проверяем, что requirements.txt существует
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt не найден"
    exit 1
fi

echo "✅ requirements.txt найден"

echo ""
echo "🎯 ГОТОВО К ДЕПЛОЮ!"
echo ""
echo "📝 Выполните следующие шаги:"
echo ""
echo "1. Откройте: $SERVICE_URL"
echo "2. Перейдите в раздел 'Manual Deploy'"
echo "3. Нажмите 'Deploy latest commit'"
echo "4. Дождитесь завершения деплоя (5-10 минут)"
echo ""
echo "🌐 Или откройте ссылку прямо сейчас:"
echo "$SERVICE_URL"
echo ""
echo "📊 После деплоя проверьте:"
echo "- Логи: render logs -r $SERVICE_ID --tail"
echo "- Health: curl https://aeon-admin-hr.onrender.com/health"
echo "- Статус: ./check-deploy-status.sh"
echo ""
echo "⏳ Ожидаемый результат:"
echo "- Приложение должно запуститься без ошибок"
echo "- Health check должен отвечать"
echo "- API endpoints должны быть доступны" 