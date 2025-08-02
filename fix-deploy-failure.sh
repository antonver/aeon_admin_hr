#!/bin/bash

echo "🔧 Исправление неудачного деплоя"
echo "================================"

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

# Проверяем текущие настройки
BUILD_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.buildCommand')
START_CMD=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.envSpecificDetails.startCommand')

echo "📋 Текущие настройки:"
echo "  Build Command: $BUILD_CMD"
echo "  Start Command: $START_CMD"

# Проверяем, нужно ли обновление
if [ "$BUILD_CMD" = "./build.sh" ] && [ "$START_CMD" = "./start.sh" ]; then
    echo "✅ Настройки уже правильные!"
    echo ""
    echo "🚀 Запускаем новый деплой..."
    echo "Перейдите в раздел 'Manual Deploy' и нажмите 'Deploy latest commit'"
    echo "Или откройте: $SERVICE_URL"
else
    echo "⚠️  Требуется обновление настроек!"
    echo ""
    echo "🔧 ПРОБЛЕМА: Сервис использует неправильные команды запуска"
    echo ""
    echo "📝 РЕШЕНИЕ: Обновите настройки в dashboard"
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
    echo "💡 АЛЬТЕРНАТИВА: Создать новый Blueprint"
    echo "1. Удалите старый сервис"
    echo "2. Создайте новый Blueprint с render.yaml"
    echo "3. Подключите репозиторий: https://github.com/antonver/aeon_admin_hr.git"
fi

echo ""
echo "📊 После исправления проверьте:"
echo "- Логи: render logs -r $SERVICE_ID --tail"
echo "- Health: curl https://aeon-admin-hr.onrender.com/health"
echo "- Статус: ./check-deploy-status.sh" 