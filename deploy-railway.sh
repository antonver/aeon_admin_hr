#!/bin/bash

# 🚀 Скрипт для деплоя на Railway
# Автор: AI Assistant
# Версия: 1.0

set -e

echo "🚀 Начинаем деплой на Railway..."

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
check_dependencies() {
    print_status "Проверяем зависимости..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git не установлен. Установите Git и попробуйте снова."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        print_warning "Docker не установлен. Установите Docker для локального тестирования."
    fi
    
    print_success "Зависимости проверены"
}

# Проверка Git репозитория
check_git_repo() {
    print_status "Проверяем Git репозиторий..."
    
    if [ ! -d ".git" ]; then
        print_error "Это не Git репозиторий. Инициализируйте Git:"
        echo "  git init"
        echo "  git add ."
        echo "  git commit -m 'Initial commit'"
        exit 1
    fi
    
    # Проверяем, есть ли удаленный репозиторий
    if ! git remote get-url origin &> /dev/null; then
        print_warning "Удаленный репозиторий не настроен."
        echo "Создайте репозиторий на GitHub и добавьте его:"
        echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "  git push -u origin main"
        exit 1
    fi
    
    print_success "Git репозиторий настроен"
}

# Проверка файлов конфигурации
check_config_files() {
    print_status "Проверяем файлы конфигурации..."
    
    required_files=("railway.json" "Dockerfile" "backend/requirements.txt" "frontend/package.json")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Файл $file не найден"
            exit 1
        fi
    done
    
    print_success "Все файлы конфигурации найдены"
}

# Локальное тестирование Docker
test_docker_build() {
    if command -v docker &> /dev/null; then
        print_status "Тестируем Docker сборку..."
        
        if docker build -t hr-admin-test . &> /dev/null; then
            print_success "Docker сборка успешна"
        else
            print_warning "Docker сборка не удалась. Проверьте Dockerfile"
        fi
    fi
}

# Проверка изменений
check_changes() {
    print_status "Проверяем изменения в репозитории..."
    
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Есть несохраненные изменения:"
        git status --short
        
        read -p "Хотите закоммитить изменения? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            git commit -m "Update for Railway deployment"
            print_success "Изменения закоммичены"
        fi
    else
        print_success "Все изменения сохранены"
    fi
}

# Отправка в GitHub
push_to_github() {
    print_status "Отправляем изменения в GitHub..."
    
    if git push origin main; then
        print_success "Код отправлен в GitHub"
    else
        print_error "Ошибка отправки в GitHub"
        exit 1
    fi
}

# Инструкции по деплою
show_deploy_instructions() {
    echo
    echo "🎯 СЛЕДУЮЩИЕ ШАГИ ДЛЯ ДЕПЛОЯ:"
    echo
    echo "1. 📱 Откройте Railway Dashboard:"
    echo "   https://railway.app"
    echo
    echo "2. 🚀 Создайте новый проект:"
    echo "   - Нажмите 'Start a New Project'"
    echo "   - Выберите 'Deploy from GitHub repo'"
    echo "   - Подключите ваш GitHub аккаунт"
    echo "   - Выберите репозиторий: $(basename $(git remote get-url origin) .git)"
    echo
    echo "3. 🗄️ Добавьте базу данных:"
    echo "   - В проекте нажмите 'New'"
    echo "   - Выберите 'Database' → 'PostgreSQL'"
    echo
    echo "4. ⚙️ Настройте переменные окружения:"
    echo "   - SECRET_KEY=your-super-secret-key-here"
    echo "   - BOT_TOKEN= (если используете Telegram)"
    echo
    echo "5. 🚀 Деплой:"
    echo "   - Railway автоматически обнаружит railway.json и Dockerfile"
    echo "   - Нажмите 'Deploy Now'"
    echo
    echo "6. 🎉 Получите доступ:"
    echo "   - URL: https://your-app-name.railway.app"
    echo "   - Логин: admin@example.com"
    echo "   - Пароль: admin123"
    echo
    echo "📚 Подробная документация: RAILWAY_DEPLOY.md"
}

# Основная функция
main() {
    echo "🚀 HR Admin System - Railway Deploy Script"
    echo "=========================================="
    echo
    
    check_dependencies
    check_git_repo
    check_config_files
    test_docker_build
    check_changes
    push_to_github
    show_deploy_instructions
    
    echo
    print_success "Скрипт завершен успешно! 🎉"
}

# Запуск скрипта
main "$@" 