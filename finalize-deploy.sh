#!/bin/bash

echo "🎯 Завершение деплоя на Render"
echo "=============================="

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
APP_URL=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.url')

echo "✅ Найден сервис: aeon_admin_hr"
echo "🌐 URL приложения: $APP_URL"

# Проверяем текущие настройки
BUILD_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.buildCommand')
START_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.startCommand')

echo "📋 Текущие настройки:"
echo "  Build Command: $BUILD_CMD"
echo "  Start Command: $START_CMD"

# Проверяем, нужно ли обновление настроек
if [ "$BUILD_CMD" != "./build.sh" ] || [ "$START_CMD" != "./start.sh" ]; then
    echo ""
    echo "⚠️  ТРЕБУЕТСЯ ОБНОВЛЕНИЕ НАСТРОЕК!"
    echo ""
    echo "🔧 Выполните следующие шаги:"
    echo ""
    echo "1. Откройте: $SERVICE_URL"
    echo "2. Перейдите в раздел 'Settings'"
    echo "3. Обновите настройки:"
    echo "   - Build Command: ./build.sh"
    echo "   - Start Command: ./start.sh"
    echo "4. Добавьте переменные окружения:"
    echo "   - BOT_TOKEN (обязательно)"
    echo "   - NOTION_TOKEN (опционально)"
    echo "   - NOTION_DATABASE_ID (опционально)"
    echo "5. Нажмите 'Save Changes'"
    echo "6. Перейдите в раздел 'Manual Deploy' и нажмите 'Deploy latest commit'"
    echo ""
    echo "🌐 Или откройте ссылку прямо сейчас:"
    echo "$SERVICE_URL"
    echo ""
    echo "⏳ После обновления настроек запустите этот скрипт снова"
    exit 1
fi

echo "✅ Настройки правильные!"

# Проверяем статус приложения
echo "🔍 Проверяем статус приложения..."
if curl -s "$APP_URL/health" > /dev/null 2>&1; then
    echo "✅ Приложение работает!"
    echo "🌐 Health check: $APP_URL/health"
else
    echo "⚠️  Приложение не отвечает"
    echo "📊 Проверяем логи..."
    echo "Логи последних ошибок:"
    render logs -r $SERVICE_ID --output text | tail -10
    echo ""
    echo "🔧 Возможные решения:"
    echo "1. Проверьте переменные окружения"
    echo "2. Перезапустите сервис: render restart $SERVICE_ID"
    echo "3. Запустите новый деплой через dashboard"
fi

echo ""
echo "🎉 Деплой завершен!"
echo ""
echo "📊 Полезные ссылки:"
echo "- Приложение: $APP_URL"
echo "- API Docs: $APP_URL/docs"
echo "- Health Check: $APP_URL/health"
echo "- Dashboard: $SERVICE_URL"
echo ""
echo "🔧 Полезные команды:"
echo "- Логи: render logs -r $SERVICE_ID --tail"
echo "- Перезапуск: render restart $SERVICE_ID"
echo "- Статус: render services"
echo ""
echo "📝 Следующие шаги:"
echo "1. Настройте переменные окружения (BOT_TOKEN и др.)"
echo "2. Протестируйте функциональность"
echo "3. Настройте автодеплой для будущих обновлений" 