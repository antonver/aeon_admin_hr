#!/bin/bash

# Скрипт для настройки Cloudflare Tunnel с авторизацией

echo "🔐 Настройка Cloudflare Tunnel с авторизацией"
echo "============================================="

# Проверяем, установлен ли cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не установлен."
    echo "Установите его:"
    echo "  macOS: brew install cloudflare/cloudflare/cloudflared"
    echo "  Linux: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared"
    exit 1
fi

echo "✅ cloudflared установлен"

# Проверяем авторизацию
echo "🔍 Проверка авторизации..."
if cloudflared tunnel list &> /dev/null; then
    echo "✅ Уже авторизован в Cloudflare"
else
    echo "⚠️  Не авторизован в Cloudflare"
    echo ""
    echo "Для авторизации выполните следующие шаги:"
    echo ""
    echo "1. Зарегистрируйтесь на https://dash.cloudflare.com"
    echo "2. Перейдите в раздел 'Zero Trust' → 'Access' → 'Tunnels'"
    echo "3. Создайте новый туннель"
    echo "4. Скопируйте команду для авторизации"
    echo ""
    echo "Или выполните авторизацию вручную:"
    echo "cloudflared tunnel login"
    echo ""
    echo "После авторизации запустите этот скрипт снова"
    exit 1
fi

# Создаем туннель
echo "🌐 Создание туннеля..."
TUNNEL_NAME="aeon-hr-admin-$(date +%s)"

echo "Создаем туннель: $TUNNEL_NAME"
cloudflared tunnel create $TUNNEL_NAME

# Получаем ID туннеля
TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')
echo "ID туннеля: $TUNNEL_ID"

# Создаем конфигурационный файл
echo "📝 Создание конфигурации..."
cat > cloudflared-auth.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: ~/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: aeon-hr-admin.your-domain.com
    service: http://localhost:8001
  - service: http_status:404
EOF

echo "✅ Конфигурация создана: cloudflared-auth.yml"
echo ""
echo "📋 Следующие шаги:"
echo "1. Настройте DNS запись для вашего домена"
echo "2. Замените 'your-domain.com' на ваш домен в cloudflared-auth.yml"
echo "3. Запустите туннель: cloudflared tunnel --config cloudflared-auth.yml run"
echo ""
echo "🎉 Настройка завершена!" 