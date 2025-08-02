#!/bin/bash

echo "🚀 Быстрое завершение деплоя"
echo "============================"

# Получаем URL dashboard
SERVICE_INFO=$(render services --output json | jq -r '.[] | select(.service.name == "aeon_admin_hr")')
DASHBOARD_URL=$(echo "$SERVICE_INFO" | jq -r '.service.dashboardUrl')
APP_URL=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.url')

echo "🌐 Открываем Render Dashboard..."
echo "URL: $DASHBOARD_URL"

# Открываем браузер
if command -v open &> /dev/null; then
    open "$DASHBOARD_URL"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$DASHBOARD_URL"
else
    echo "⚠️  Не удалось открыть браузер автоматически"
    echo "Откройте ссылку вручную: $DASHBOARD_URL"
fi

echo ""
echo "📋 Быстрые шаги для завершения:"
echo ""
echo "1. В открывшемся dashboard перейдите в 'Settings'"
echo "2. Измените настройки:"
echo "   - Build Command: ./build.sh"
echo "   - Start Command: ./start.sh"
echo "3. Добавьте переменные окружения:"
echo "   - BOT_TOKEN (ваш токен Telegram бота)"
echo "4. Нажмите 'Save Changes'"
echo "5. Перейдите в 'Manual Deploy' → 'Deploy latest commit'"
echo ""
echo "⏳ После завершения деплоя проверьте:"
echo "curl $APP_URL/health"
echo ""
echo "🎯 Или запустите: ./finalize-deploy.sh" 