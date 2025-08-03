#!/bin/bash

echo "🔧 Исправление и деплой"
echo "======================"

# Проверяем авторизацию
echo "🔐 Проверяем авторизацию..."
if ! render whoami > /dev/null 2>&1; then
    echo "❌ Не авторизованы в Render. Выполните: render login"
    exit 1
fi

echo "✅ Авторизованы в Render"

# Проверяем, что app.py существует и исправлен
if [ ! -f "app.py" ]; then
    echo "❌ app.py не найден"
    exit 1
fi

echo "✅ app.py найден"

# Проверяем, что requirements.txt существует
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt не найден"
    exit 1
fi

echo "✅ requirements.txt найден"

# Пушим изменения
echo "📤 Пушим изменения в GitHub..."
git add .
git commit -m "Исправлен app.py для правильной работы с импортами"
git push origin main

echo "✅ Код обновлен в GitHub!"

# Получаем информацию о сервисе
SERVICE_INFO=$(render services --output json | jq -r '.[] | select(.service.name == "aeon_admin_hr")')
SERVICE_URL=$(echo "$SERVICE_INFO" | jq -r '.service.dashboardUrl')

echo ""
echo "🎯 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "📝 Теперь выполните:"
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
echo "- Логи: render logs -r srv-d272anh5pdvs73c1hdpg --tail"
echo "- Health: curl https://aeon-admin-hr.onrender.com/health"
echo "- Статус: ./check-deploy-status.sh" 