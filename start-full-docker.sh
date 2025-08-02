#!/bin/bash

# 🚀 Полный запуск HR Admin System с Docker и Cloudflare Tunnel
# Этот скрипт запускает все компоненты в Docker и настраивает внешний доступ

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}🚀 $1${NC}"
}

# Проверка зависимостей
check_dependencies() {
    print_header "Проверка зависимостей..."
    
    # Проверка Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker не установлен. Установите Docker Desktop."
        exit 1
    fi
    
    # Проверка Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose не установлен. Установите Docker Compose."
        exit 1
    fi
    
    # Проверка cloudflared
    if ! command -v cloudflared &> /dev/null; then
        print_warning "cloudflared не установлен. Устанавливаем..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install cloudflare/cloudflare/cloudflared
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
            sudo dpkg -i cloudflared-linux-amd64.deb
            rm cloudflared-linux-amd64.deb
        else
            print_error "Неизвестная ОС. Установите cloudflared вручную."
            exit 1
        fi
    fi
    
    print_success "Все зависимости установлены"
}

# Остановка существующих контейнеров
stop_existing_containers() {
    print_header "Остановка существующих контейнеров..."
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose down
        print_success "Существующие контейнеры остановлены"
    else
        print_info "Нет запущенных контейнеров"
    fi
}

# Сборка и запуск Docker контейнеров
start_docker_services() {
    print_header "Запуск Docker сервисов..."
    
    # Сборка образов
    print_info "Сборка Docker образов..."
    docker-compose build --no-cache
    
    # Запуск сервисов
    print_info "Запуск сервисов..."
    docker-compose up -d
    
    # Ожидание готовности базы данных
    print_info "Ожидание готовности базы данных..."
    sleep 10
    
    # Проверка статуса контейнеров
    print_info "Проверка статуса контейнеров..."
    docker-compose ps
    
    print_success "Docker сервисы запущены"
}

# Проверка работоспособности API
check_api_health() {
    print_header "Проверка работоспособности API..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8000/api/health > /dev/null; then
            print_success "API работает"
            return 0
        fi
        
        print_info "Попытка $attempt/$max_attempts - API еще не готов..."
        sleep 2
        ((attempt++))
    done
    
    print_error "API не отвечает после $max_attempts попыток"
    return 1
}

# Настройка Cloudflare Tunnel
setup_cloudflare_tunnel() {
    print_header "Настройка Cloudflare Tunnel..."
    
    # Останавливаем существующие туннели
    if [ -f ".cloudflared.pid" ] || [ -f ".cloudflared-backend.pid" ] || [ -f ".cloudflared-frontend.pid" ]; then
        print_info "Остановка существующих туннелей..."
        ./stop-cloudflare.sh > /dev/null 2>&1
    fi
    
    # Запускаем туннели для backend и frontend
    print_info "Запуск туннелей..."
    
    # Backend API туннель
    cloudflared tunnel --url http://localhost:8000 > cloudflared-backend.log 2>&1 &
    local backend_pid=$!
    echo $backend_pid > .cloudflared-backend.pid
    
    # Frontend туннель
    cloudflared tunnel --url http://localhost:3002 > cloudflared-frontend.log 2>&1 &
    local frontend_pid=$!
    echo $frontend_pid > .cloudflared-frontend.pid
    
    # Ожидание запуска туннелей
    sleep 5
    
    if kill -0 $backend_pid 2>/dev/null && kill -0 $frontend_pid 2>/dev/null; then
        print_success "Cloudflare Tunnel запущен"
        
        # Получаем URL туннелей
        local backend_url=$(grep -o "https://.*trycloudflare.com" cloudflared-backend.log 2>/dev/null | head -1)
        local frontend_url=$(grep -o "https://.*trycloudflare.com" cloudflared-frontend.log 2>/dev/null | head -1)
        
        if [ -n "$backend_url" ]; then
            print_success "Backend API: $backend_url"
        fi
        
        if [ -n "$frontend_url" ]; then
            print_success "Frontend: $frontend_url"
        fi
    else
        print_error "Ошибка запуска Cloudflare Tunnel"
        return 1
    fi
}

# Показ информации о доступе
show_access_info() {
    print_header "Информация о доступе"
    
    echo ""
    echo "📱 Локальный доступ:"
    echo "   Frontend: http://localhost:3002"
    echo "   Backend API: http://localhost:8000"
    echo "   API документация: http://localhost:8000/docs"
    echo "   Проверка здоровья: http://localhost:8000/api/health"
    echo ""
    
    # Получаем публичный IP
    local public_ip=$(curl -s ifconfig.me 2>/dev/null || echo "неизвестен")
    echo "🌐 Внешний доступ:"
    echo "   Ваш IP: $public_ip"
    echo "   Прямой доступ: http://$public_ip:8000 (если порт открыт)"
    echo ""
    
    echo "🔧 Управление:"
    echo "   Остановка: ./stop-full-docker.sh"
    echo "   Логи: docker-compose logs -f"
    echo "   Статус: docker-compose ps"
    echo ""
    
    echo "📊 Cloudflare Tunnel:"
    echo "   Backend API: $(grep -o 'https://.*trycloudflare.com' cloudflared-backend.log 2>/dev/null | head -1 || echo 'не готов')"
    echo "   Frontend: $(grep -o 'https://.*trycloudflare.com' cloudflared-frontend.log 2>/dev/null | head -1 || echo 'не готов')"
    echo "   Логи backend: tail -f cloudflared-backend.log"
    echo "   Логи frontend: tail -f cloudflared-frontend.log"
    echo "   Остановка туннелей: ./stop-cloudflare.sh"
    echo ""
}

# Основная функция
main() {
    print_header "Запуск HR Admin System с Docker и Cloudflare Tunnel"
    
    # Проверка зависимостей
    check_dependencies
    
    # Остановка существующих контейнеров
    stop_existing_containers
    
    # Запуск Docker сервисов
    start_docker_services
    
    # Проверка API
    if ! check_api_health; then
        print_error "Не удалось запустить API. Проверьте логи: docker-compose logs backend"
        exit 1
    fi
    
    # Настройка Cloudflare Tunnel
    if setup_cloudflare_tunnel; then
        print_success "Cloudflare Tunnel настроен"
    else
        print_warning "Cloudflare Tunnel не настроен. Настройте вручную."
    fi
    
    # Показ информации
    show_access_info
    
    print_success "🎉 Система полностью запущена!"
    print_info "Для остановки используйте: ./stop-full-docker.sh"
}

# Обработка сигналов
cleanup() {
    print_info "Получен сигнал остановки..."
    if [ -f ".cloudflared.pid" ]; then
        local tunnel_pid=$(cat .cloudflared.pid)
        if kill -0 $tunnel_pid 2>/dev/null; then
            kill $tunnel_pid
            print_info "Cloudflare Tunnel остановлен"
        fi
        rm -f .cloudflared.pid
    fi
    exit 0
}

# Установка обработчиков сигналов
trap cleanup SIGINT SIGTERM

# Запуск основной функции
main "$@" 