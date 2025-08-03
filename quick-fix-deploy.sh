#!/bin/bash

echo "🔧 Быстрое исправление деплоя"
echo "============================="

# Проверяем авторизацию
echo "🔐 Проверяем авторизацию..."
if ! render whoami > /dev/null 2>&1; then
    echo "❌ Не авторизованы в Render. Выполните: render login"
    exit 1
fi

echo "✅ Авторизованы в Render"

# Создаем app.py если его нет
if [ ! -f "app.py" ]; then
    echo "📝 Создаем app.py для совместимости..."
    cat > app.py << 'EOF'
"""
WSGI приложение для совместимости с Render
Импортирует FastAPI приложение из backend/main.py
"""

import sys
import os

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Импортируем FastAPI приложение
from main import app

# Создаем WSGI приложение для gunicorn
application = app
EOF
    echo "✅ app.py создан"
else
    echo "✅ app.py уже существует"
fi

# Проверяем requirements.txt
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt найден"
else
    echo "📝 Копируем requirements.txt из backend..."
    cp backend/requirements.txt .
    echo "✅ requirements.txt скопирован"
fi

# Пушим изменения
echo "📤 Пушим изменения в GitHub..."
git add .
git commit -m "Быстрое исправление деплоя - добавлен app.py"
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
echo "4. Дождитесь завершения деплоя"
echo ""
echo "🌐 Или откройте ссылку прямо сейчас:"
echo "$SERVICE_URL"
echo ""
echo "📊 После деплоя проверьте:"
echo "- Логи: render logs -r srv-d272anh5pdvs73c1hdpg --tail"
echo "- Health: curl https://aeon-admin-hr.onrender.com/health"
echo "- Статус: ./check-deploy-status.sh" 