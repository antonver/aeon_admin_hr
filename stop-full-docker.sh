#!/bin/bash

# 🛑 Остановка HR Admin System с Docker и Cloudflare Tunnel

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
    echo -e "${BLUE}🛑 $1${NC}"
}

# Остановка Cloudflare Tunnel
stop_cloudflare_tunnel() {
    print_header "Остановка Cloudflare Tunnel..."
    
    if [ -f ".cloudflared.pid" ]; then
        local tunnel_pid=$(cat .cloudflared.pid)
        if kill -0 $tunnel_pid 2>/dev/null; then
            kill $tunnel_pid
            print_success "Cloudflare Tunnel остановлен (PID: $tunnel_pid)"
        else
            print_warning "Cloudflare Tunnel уже остановлен"
        fi
        rm -f .cloudflared.pid
    else
        print_info "Cloudflare Tunnel не запущен"
    fi
}

# Остановка Docker контейнеров
stop_docker_containers() {
    print_header "Остановка Docker контейнеров..."
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose down
        print_success "Docker контейнеры остановлены"
    else
        print_info "Docker контейнеры уже остановлены"
    fi
}

# Очистка ресурсов
cleanup_resources() {
    print_header "Очистка ресурсов..."
    
    # Удаление неиспользуемых образов (опционально)
    read -p "Удалить неиспользуемые Docker образы? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker image prune -f
        print_success "Неиспользуемые образы удалены"
    fi
    
    # Удаление неиспользуемых томов (опционально)
    read -p "Удалить неиспользуемые Docker тома? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
        print_success "Неиспользуемые тома удалены"
    fi
}

# Основная функция
main() {
    print_header "Остановка HR Admin System"
    
    # Остановка Cloudflare Tunnel
    stop_cloudflare_tunnel
    
    # Остановка Docker контейнеров
    stop_docker_containers
    
    # Очистка ресурсов
    cleanup_resources
    
    print_success "🎉 Система полностью остановлена!"
    print_info "Для запуска используйте: ./start-full-docker.sh"
}

# Запуск основной функции
main "$@" 