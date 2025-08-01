#!/bin/bash

echo "🚀 Запуск Cloudflare Tunnel (исправленная версия)"
echo "=================================================="

# Проверяем, что backend работает
echo "📡 Проверка backend..."
if ! curl -s http://localhost:8001/api/health > /dev/null; then
    echo "❌ Backend не работает на порту 8001"
    echo "Запустите сначала: ./start-backend.sh"
    exit 1
fi

echo "✅ Backend работает"

# Останавливаем существующие процессы
echo "🛑 Остановка существующих процессов..."
pkill -f cloudflared 2>/dev/null
sleep 2

# Пробуем разные варианты запуска Cloudflare Tunnel
echo "🌐 Попытка создания Cloudflare Tunnel..."

# Вариант 1: Простой туннель без авторизации
echo "Попытка 1: Простой туннель..."
cloudflared tunnel --url http://localhost:8001 --logfile cloudflared-attempt1.log &
TUNNEL_PID=$!

# Ждем и проверяем результат
sleep 10
if grep -q "https://.*trycloudflare.com" cloudflared-attempt1.log; then
    echo "✅ Туннель создан успешно!"
    TUNNEL_URL=$(grep "https://.*trycloudflare.com" cloudflared-attempt1.log | tail -1 | sed 's/.*https/https/')
    echo "📱 Внешний адрес админки: $TUNNEL_URL"
    echo ""
    echo "🔗 Доступные endpoints:"
    echo "   $TUNNEL_URL"
    echo "   $TUNNEL_URL/api/health"
    echo "   $TUNNEL_URL/api/external/health"
    echo "   $TUNNEL_URL/test-external-api"
    echo ""
    echo "🛑 Для остановки нажмите Ctrl+C"
    wait $TUNNEL_PID
    exit 0
fi

# Если первый вариант не сработал, пробуем второй
echo "Попытка 2: Туннель с отключенной проверкой сертификатов..."
kill $TUNNEL_PID 2>/dev/null
sleep 2

# Устанавливаем переменные окружения для обхода проблем с сертификатами
export CLOUDFLARE_TUNNEL_ORIGIN_CERT=""
export CLOUDFLARE_TUNNEL_NO_TLS_VERIFY="true"

cloudflared tunnel --url http://localhost:8001 --no-tls-verify --logfile cloudflared-attempt2.log &
TUNNEL_PID=$!

# Ждем и проверяем результат
sleep 15
if grep -q "https://.*trycloudflare.com" cloudflared-attempt2.log; then
    echo "✅ Туннель создан успешно!"
    TUNNEL_URL=$(grep "https://.*trycloudflare.com" cloudflared-attempt2.log | tail -1 | sed 's/.*https/https/')
    echo "📱 Внешний адрес админки: $TUNNEL_URL"
    echo ""
    echo "🔗 Доступные endpoints:"
    echo "   $TUNNEL_URL"
    echo "   $TUNNEL_URL/api/health"
    echo "   $TUNNEL_URL/api/external/health"
    echo "   $TUNNEL_URL/test-external-api"
    echo ""
    echo "🛑 Для остановки нажмите Ctrl+C"
    wait $TUNNEL_PID
    exit 0
fi

# Если и второй вариант не сработал, предлагаем альтернативы
echo "❌ Не удалось создать Cloudflare Tunnel"
echo ""
echo "🔍 Возможные причины:"
echo "   - Проблемы с сетевым подключением"
echo "   - Блокировка Cloudflare в вашей сети"
echo "   - Проблемы с сертификатами"
echo ""
echo "💡 Альтернативные решения:"
echo "1. Используйте Localtunnel: ./start-localtunnel.sh"
echo "2. Настройте Ngrok с авторизацией"
echo "3. Используйте прямой доступ: http://46.211.115.16:8001"
echo ""
echo "📋 Логи попыток:"
echo "   cloudflared-attempt1.log"
echo "   cloudflared-attempt2.log"

kill $TUNNEL_PID 2>/dev/null
exit 1 