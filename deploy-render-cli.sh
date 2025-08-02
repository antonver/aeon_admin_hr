#!/bin/bash

echo "🚀 Деплой на Render через CLI"
echo "============================"

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

# Пушим изменения
echo "📤 Пушим изменения в GitHub..."
git add .
git commit -m "Обновление для Render деплоя $(date)"
git push origin main

echo "✅ Код обновлен в GitHub!"

# Проверяем существующие сервисы
echo "🔍 Проверяем существующие сервисы..."
EXISTING_SERVICES=$(render services --output json | jq -r '.[].service.name')

if echo "$EXISTING_SERVICES" | grep -q "aeon_admin_hr"; then
    echo "⚠️  Сервис aeon_admin_hr уже существует"
    echo "📝 Рекомендуется:"
    echo "1. Удалить старый сервис через dashboard.render.com"
    echo "2. Создать новый Blueprint с render.yaml"
    echo ""
    echo "Или обновить существующий сервис вручную:"
    echo "- Изменить build command на: ./build.sh"
    echo "- Изменить start command на: ./start.sh"
    echo "- Добавить переменные окружения"
else
    echo "✅ Готов к созданию новых сервисов"
fi

echo ""
echo "📝 Следующие шаги:"
echo ""
echo "Вариант 1 - Через Dashboard (рекомендуется):"
echo "1. Зайдите на https://dashboard.render.com"
echo "2. Нажмите 'New +' → 'Blueprint'"
echo "3. Подключите репозиторий: https://github.com/antonver/aeon_admin_hr.git"
echo "4. Выберите файл render.yaml"
echo "5. Нажмите 'Apply'"
echo ""
echo "Вариант 2 - Обновить существующий сервис:"
echo "1. Зайдите на https://dashboard.render.com/web/srv-d272anh5pdvs73c1hdpg"
echo "2. В разделе 'Settings' обновите:"
echo "   - Build Command: ./build.sh"
echo "   - Start Command: ./start.sh"
echo "3. Добавьте переменные окружения"
echo "4. Нажмите 'Save Changes'"
echo ""
echo "🔧 Обязательные переменные окружения:"
echo "- BOT_TOKEN (токен Telegram бота)"
echo ""
echo "📖 Подробные инструкции: RENDER_DEPLOYMENT.md" 