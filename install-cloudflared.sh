#!/bin/bash

# Скрипт для установки cloudflared

echo "🔧 Установка cloudflared..."

# Определяем операционную систему
OS=$(uname -s)
ARCH=$(uname -m)

case $OS in
    "Darwin")
        echo "📦 Установка для macOS..."
        if command -v brew &> /dev/null; then
            brew install cloudflare/cloudflare/cloudflared
        else
            echo "❌ Homebrew не установлен. Установите его с https://brew.sh/"
            exit 1
        fi
        ;;
    "Linux")
        echo "📦 Установка для Linux..."
        # Скачиваем последнюю версию
        LATEST_VERSION=$(curl -s https://api.github.com/repos/cloudflare/cloudflared/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
        wget -O cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/download/${LATEST_VERSION}/cloudflared-linux-amd64.deb"
        sudo dpkg -i cloudflared.deb
        rm cloudflared.deb
        ;;
    *)
        echo "❌ Неподдерживаемая операционная система: $OS"
        echo "Установите cloudflared вручную: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
        ;;
esac

# Проверяем установку
if command -v cloudflared &> /dev/null; then
    echo "✅ cloudflared успешно установлен!"
    echo "Версия: $(cloudflared version)"
    echo ""
    echo "Следующие шаги:"
    echo "1. Создайте туннель: cloudflared tunnel create aeon-hr-admin"
    echo "2. Настройте cloudflared.yml"
    echo "3. Запустите: ./start-cloudflare.sh"
else
    echo "❌ Ошибка установки cloudflared"
    exit 1
fi 