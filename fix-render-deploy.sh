#!/bin/bash

echo "🔧 Исправление проблем с автодеплоем на Render"
echo "=============================================="

# Проверяем авторизацию
echo "🔐 Проверяем авторизацию..."
if ! render whoami > /dev/null 2>&1; then
    echo "❌ Не авторизованы в Render. Выполните: render login"
    exit 1
fi

echo "✅ Авторизованы в Render"

# Проверяем существующий сервис
echo "🔍 Проверяем существующий сервис..."
SERVICE_INFO=$(render services --output json | jq -r '.[] | select(.service.name == "aeon_admin_hr")')

if [ -z "$SERVICE_INFO" ]; then
    echo "❌ Сервис aeon_admin_hr не найден"
    echo "📝 Создайте новый Blueprint через dashboard.render.com"
    exit 1
fi

SERVICE_ID=$(echo "$SERVICE_INFO" | jq -r '.service.id')
SERVICE_URL=$(echo "$SERVICE_INFO" | jq -r '.service.dashboardUrl')

echo "✅ Найден сервис: aeon_admin_hr (ID: $SERVICE_ID)"
echo "🌐 Dashboard URL: $SERVICE_URL"

# Проверяем текущие настройки
echo "🔍 Проверяем текущие настройки..."
BUILD_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.buildCommand')
START_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.startCommand')

echo "📋 Текущие настройки:"
echo "  Build Command: $BUILD_CMD"
echo "  Start Command: $START_CMD"

# Проверяем, нужно ли обновление
NEEDS_UPDATE=false

if [ "$BUILD_CMD" != "./build.sh" ]; then
    echo "⚠️  Build Command нужно обновить на: ./build.sh"
    NEEDS_UPDATE=true
fi

if [ "$START_CMD" != "./start.sh" ]; then
    echo "⚠️  Start Command нужно обновить на: ./start.sh"
    NEEDS_UPDATE=true
fi

if [ "$NEEDS_UPDATE" = true ]; then
    echo ""
    echo "🔧 Требуется обновление настроек!"
    echo ""
    echo "📝 Выполните следующие шаги:"
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
else
    echo "✅ Настройки уже правильные!"
    echo ""
    echo "🚀 Запускаем новый деплой..."
    echo "Перейдите в раздел 'Manual Deploy' и нажмите 'Deploy latest commit'"
    echo "Или откройте: $SERVICE_URL"
fi

echo ""
echo "📊 Дополнительная информация:"
echo "- Логи деплоя: render logs $SERVICE_ID"
echo "- Статус сервиса: render services"
echo "- Health check: $(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.url')/health" 