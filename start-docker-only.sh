#!/bin/bash

# 🐳 Запуск HR Admin System только с Docker (без Cloudflare Tunnel)

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
    echo -e "${BLUE}🐳 $1${NC}"
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
    sleep 15
    
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
    echo "   Остановка: docker-compose down"
    echo "   Логи: docker-compose logs -f"
    echo "   Статус: docker-compose ps"
    echo "   Перезапуск: docker-compose restart"
    echo ""
    
    echo "📊 База данных:"
    echo "   PostgreSQL: localhost:5432"
    echo "   Пользователь: postgres"
    echo "   Пароль: password"
    echo "   База данных: hr_admin"
    echo ""
}

# Основная функция
main() {
    print_header "Запуск HR Admin System с Docker"
    
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
    
    # Показ информации
    show_access_info
    
    print_success "🎉 Система запущена!"
    print_info "Для остановки используйте: docker-compose down"
}

# Запуск основной функции
main "$@" 