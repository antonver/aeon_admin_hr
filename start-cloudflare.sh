#!/bin/bash

# Скрипт для запуска приложения с Cloudflare Tunnel

echo "🚀 Запуск приложения с Cloudflare Tunnel..."

# Проверяем, установлен ли cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не установлен. Установите его с https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
    exit 1
fi

# Проверяем наличие конфигурационного файла
if [ ! -f "cloudflared.yml" ]; then
    echo "❌ Файл cloudflared.yml не найден. Создайте его с вашими настройками."
    exit 1
fi

# Запускаем backend
echo "📦 Запуск backend..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Ждем немного, чтобы backend запустился
sleep 3

# Запускаем frontend (если нужно)
echo "🎨 Запуск frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

# Ждем немного, чтобы frontend запустился
sleep 5

# Запускаем Cloudflare Tunnel
echo "🌐 Запуск Cloudflare Tunnel..."
cloudflared tunnel --config ../cloudflared.yml run

# Очистка при завершении
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT 