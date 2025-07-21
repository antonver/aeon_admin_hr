#!/bin/bash

echo "🚀 Запуск HR Admin Panel..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cat > .env << EOF
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Notion
NOTION_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_candidates_database_id_here
NOTION_TASKS_DATABASE_ID=your_tasks_database_id_here
EOF
    echo "⚠️  Пожалуйста, настройте переменные окружения в файле .env"
fi

# Запуск проекта
echo "🔧 Запуск сервисов..."
docker-compose up --build -d

echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса
echo "📊 Статус сервисов:"
docker-compose ps

echo ""
echo "✅ HR Admin Panel запущен!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "Для остановки используйте: docker-compose down" 