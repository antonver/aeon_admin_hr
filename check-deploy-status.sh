#!/bin/bash

echo "🔍 Проверка статуса деплоя"
echo "=========================="

# Получаем информацию о сервисе
SERVICE_INFO=$(render services --output json | jq -r '.[] | select(.service.name == "aeon_admin_hr")')
APP_URL=$(echo "$SERVICE_INFO" | jq -r '.service.serviceDetails.url')
SERVICE_ID=$(echo "$SERVICE_INFO" | jq -r '.service.id')

echo "🌐 URL приложения: $APP_URL"

# Проверяем health endpoint
echo "🔍 Проверяем health endpoint..."
HEALTH_RESPONSE=$(curl -s "$APP_URL/health" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$HEALTH_RESPONSE" ]; then
    echo "✅ Health check успешен!"
    echo "📋 Ответ: $HEALTH_RESPONSE"
else
    echo "⚠️  Health check не отвечает"
    echo "📊 Проверяем логи..."
    echo "Последние логи:"
    render logs -r $SERVICE_ID --output text | tail -5
fi

# Проверяем основную страницу
echo ""
echo "🔍 Проверяем основную страницу..."
MAIN_RESPONSE=$(curl -s "$APP_URL/" 2>/dev/null | head -c 100)

if [ $? -eq 0 ] && [ -n "$MAIN_RESPONSE" ]; then
    echo "✅ Основная страница загружается!"
    echo "📋 Начало ответа: $MAIN_RESPONSE..."
else
    echo "⚠️  Основная страница не отвечает"
fi

# Проверяем API docs
echo ""
echo "🔍 Проверяем API документацию..."
DOCS_RESPONSE=$(curl -s "$APP_URL/docs" 2>/dev/null | head -c 100)

if [ $? -eq 0 ] && [ -n "$DOCS_RESPONSE" ]; then
    echo "✅ API документация доступна!"
    echo "📋 URL: $APP_URL/docs"
else
    echo "⚠️  API документация недоступна"
fi

echo ""
echo "📊 Итоговый статус:"
echo "🌐 Приложение: $APP_URL"
echo "📚 API Docs: $APP_URL/docs"
echo "🏥 Health Check: $APP_URL/health"
echo "📊 Dashboard: https://dashboard.render.com/web/$SERVICE_ID"

if [ $? -eq 0 ] && [ -n "$HEALTH_RESPONSE" ]; then
    echo ""
    echo "🎉 Деплой успешно завершен!"
    echo "✅ Приложение работает корректно"
else
    echo ""
    echo "⚠️  Требуется дополнительная настройка"
    echo "📝 Проверьте логи и переменные окружения"
fi 