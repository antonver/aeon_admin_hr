#!/bin/bash

# Простой скрипт для запуска Cloudflare Tunnel
echo "🌐 Запуск Cloudflare Tunnel..."

# Проверяем, установлен ли cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не установлен."
    echo "Установите: brew install cloudflare/cloudflare/cloudflared"
    exit 1
fi

# Останавливаем существующий туннель
if [ -f .cloudflared.pid ]; then
    echo "🛑 Остановка существующего туннеля..."
    kill $(cat .cloudflared.pid) 2>/dev/null
    rm -f .cloudflared.pid
fi

# Запускаем новый туннель
echo "🚀 Запуск туннеля для backend API..."
cloudflared tunnel --url http://localhost:8000 > cloudflared-backend.log 2>&1 &
echo $! > .cloudflared-backend.pid

echo "🚀 Запуск туннеля для frontend..."
cloudflared tunnel --url http://localhost:3002 > cloudflared-frontend.log 2>&1 &
echo $! > .cloudflared-frontend.pid

echo "⏳ Ожидание запуска туннелей..."
sleep 5

# Показываем логи для получения URL
echo ""
echo "📋 Backend API туннель:"
echo "Логи: tail -f cloudflared-backend.log"
echo ""

echo "📋 Frontend туннель:"
echo "Логи: tail -f cloudflared-frontend.log"
echo ""

echo "🔍 Поиск URL в логах..."
echo "Backend API URL:"
grep -o "https://.*trycloudflare.com" cloudflared-backend.log 2>/dev/null || echo "URL пока не доступен, проверьте логи"

echo ""
echo "Frontend URL:"
grep -o "https://.*trycloudflare.com" cloudflared-frontend.log 2>/dev/null || echo "URL пока не доступен, проверьте логи"

echo ""
echo "✅ Туннели запущены!"
echo "Для остановки: ./stop-cloudflare.sh" 