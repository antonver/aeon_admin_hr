#!/bin/bash

echo "🌐 Проверка внешнего доступа к HR Admin System"
echo "================================================"

# Проверяем, что backend работает
echo "📡 Проверка backend..."
if curl -s http://localhost:8001/api/health > /dev/null; then
    echo "✅ Backend работает на http://localhost:8001"
else
    echo "❌ Backend не работает"
    echo "Запустите: ./start-backend.sh"
    exit 1
fi

# Проверяем IP адрес
echo ""
echo "🌍 Ваш IP адрес:"
curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "Не удалось определить"

# Проверяем открытые порты
echo ""
echo "🔍 Проверка открытых портов..."
if command -v lsof >/dev/null 2>&1; then
    echo "Порт 8001:"
    lsof -i :8001 2>/dev/null || echo "Порт 8001 не открыт"
fi

echo ""
echo "📋 Варианты настройки внешнего доступа:"
echo ""
echo "1. 🌐 Cloudflare Tunnel (рекомендуется):"
echo "   - Установите: brew install cloudflare/cloudflare/cloudflared"
echo "   - Авторизуйтесь: cloudflared tunnel login"
echo "   - Создайте туннель: cloudflared tunnel create aeon-hr-admin"
echo "   - Запустите: cloudflared tunnel --config cloudflared.yml run"
echo ""
echo "2. 🚀 Ngrok (альтернатива):"
echo "   - Установите: brew install ngrok"
echo "   - Авторизуйтесь: ngrok authtoken YOUR_TOKEN"
echo "   - Запустите: ngrok http 8001"
echo ""
echo "3. 🌍 Прямой доступ (если есть публичный IP):"
echo "   - Настройте роутер для проброса порта 8001"
echo "   - Используйте ваш публичный IP: http://YOUR_IP:8001"
echo ""
echo "4. ☁️ Облачный хостинг:"
echo "   - Heroku, Railway, Render или другие платформы"
echo "   - Загрузите код и настройте переменные окружения"
echo ""
echo "🔗 Локальный доступ: http://localhost:8001"
echo "📚 Документация: README.md" 