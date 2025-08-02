#!/bin/bash

echo "🛑 Остановка Cloudflare Tunnel..."

# Останавливаем backend туннель
if [ -f .cloudflared-backend.pid ]; then
    echo "🛑 Остановка backend туннеля..."
    kill $(cat .cloudflared-backend.pid) 2>/dev/null
    rm -f .cloudflared-backend.pid
fi

# Останавливаем frontend туннель
if [ -f .cloudflared-frontend.pid ]; then
    echo "🛑 Остановка frontend туннеля..."
    kill $(cat .cloudflared-frontend.pid) 2>/dev/null
    rm -f .cloudflared-frontend.pid
fi

# Останавливаем общий туннель
if [ -f .cloudflared.pid ]; then
    echo "🛑 Остановка общего туннеля..."
    kill $(cat .cloudflared.pid) 2>/dev/null
    rm -f .cloudflared.pid
fi

# Убиваем все процессы cloudflared
echo "🧹 Очистка процессов cloudflared..."
pkill -f cloudflared 2>/dev/null

echo "✅ Cloudflare Tunnel остановлен!" 