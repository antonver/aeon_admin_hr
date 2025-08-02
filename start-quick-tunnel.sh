#!/bin/bash

# Скрипт для запуска приложения с быстрым Cloudflare Tunnel

echo "🚀 Запуск приложения с быстрым Cloudflare Tunnel..."

# Проверяем, установлен ли cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не установлен. Установите его с https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
    exit 1
fi

# Запускаем backend
echo "📦 Запуск backend..."
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!

# Ждем немного, чтобы backend запустился
sleep 3

# Запускаем быстрый Cloudflare Tunnel
echo "🌐 Запуск быстрого Cloudflare Tunnel..."
echo "📱 Приложение будет доступно по URL, который покажет Cloudflare Tunnel"
echo ""

# Запускаем туннель напрямую к порту 8001
cloudflared tunnel --url http://localhost:8001

# Очистка при завершении
trap "kill $BACKEND_PID 2>/dev/null" EXIT 