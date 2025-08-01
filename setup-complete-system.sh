#!/bin/bash

echo "🚀 Полная настройка HR Admin System"
echo "==================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка зависимостей
print_status "Проверка зависимостей..."

# Проверяем Python
if command -v python3 &> /dev/null; then
    print_success "Python 3 установлен"
else
    print_error "Python 3 не установлен"
    exit 1
fi

# Проверяем Node.js
if command -v node &> /dev/null; then
    print_success "Node.js установлен"
else
    print_error "Node.js не установлен"
    exit 1
fi

# Проверяем cloudflared
if command -v cloudflared &> /dev/null; then
    print_success "cloudflared установлен"
else
    print_warning "cloudflared не установлен. Установите: brew install cloudflare/cloudflare/cloudflared"
fi

# Проверяем ngrok
if command -v ngrok &> /dev/null; then
    print_success "ngrok установлен"
else
    print_warning "ngrok не установлен. Установите: brew install ngrok"
fi

echo ""

# Запуск backend
print_status "Запуск backend..."
if ./start-backend.sh &> /dev/null & then
    BACKEND_PID=$!
    sleep 5
    
    # Проверяем, что backend работает
    if curl -s http://localhost:8001/api/health > /dev/null; then
        print_success "Backend запущен на http://localhost:8001"
    else
        print_error "Backend не запустился"
        exit 1
    fi
else
    print_error "Не удалось запустить backend"
    exit 1
fi

echo ""

# Тестирование API
print_status "Тестирование внешнего API..."
if ./test-external-api.sh &> /dev/null; then
    print_success "Внешний API работает корректно"
else
    print_warning "Проблемы с внешним API"
fi

echo ""

# Информация о системе
print_status "Информация о системе:"
echo "🌍 Ваш IP адрес: $(curl -s ifconfig.me 2>/dev/null || echo 'Не определен')"
echo "🔗 Локальный доступ: http://localhost:8001"
echo "📚 API документация: http://localhost:8001/docs"
echo "🧪 Тестовый интерфейс: http://localhost:8001/test-external-api"

echo ""

# Варианты внешнего доступа
print_status "Варианты настройки внешнего доступа:"
echo ""
echo "1. 🌐 Cloudflare Tunnel (рекомендуется):"
echo "   ./start-cloudflare.sh"
echo ""
echo "2. 🚀 Ngrok:"
echo "   ./setup-ngrok-tunnel.sh"
echo ""
echo "3. 🌍 Прямой доступ:"
echo "   Настройте проброс порта 8001 в роутере"
echo "   Используйте: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_IP'):8001"

echo ""

# Демо файлы
print_status "Демо файлы:"
echo "📄 external-api-demo.html - Веб-интерфейс для тестирования API"
echo "📄 EXTERNAL_API_GUIDE.md - Документация внешнего API"
echo "📄 EXTERNAL_ACCESS_GUIDE.md - Руководство по внешнему доступу"

echo ""

# Полезные команды
print_status "Полезные команды:"
echo "🔍 ./check-external-access.sh - Проверка статуса"
echo "🧪 ./test-external-api.sh - Тестирование API"
echo "📊 curl http://localhost:8001/api/health - Проверка здоровья"
echo "🛑 kill $BACKEND_PID - Остановка backend"

echo ""

print_success "Настройка завершена! 🎉"
echo ""
echo "📱 Следующие шаги:"
echo "1. Откройте http://localhost:8001 в браузере"
echo "2. Настройте внешний доступ (выберите один из вариантов выше)"
echo "3. Протестируйте внешний API через external-api-demo.html"
echo "4. Интегрируйте API с внешними сайтами" 