# HR Admin Panel - Telegram Mini Apps

## 🎯 Обзор

HR Admin Panel с аутентификацией через Telegram Mini Apps и возможностью деплоя на Heroku.

### ✅ Реализованные функции

1. **Telegram Mini Apps Аутентификация**
   - Бесшовная аутентификация через Telegram
   - Автоматическое назначение первого пользователя администратором
   - Валидация `init_data` от Telegram

2. **Управление администраторами**
   - Страница управления админами (`/admins`)
   - Добавление новых администраторов по Telegram username
   - Проверка прав доступа

3. **Docker & Heroku Deploy**
   - Полная контейнеризация с Docker Compose
   - Готовность к деплою на Heroku
   - Автоматическая инициализация базы данных

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd aeon_admin_hr-1
```

2. **Создайте .env файл**
```bash
cp env.example .env
# Отредактируйте .env файл при необходимости
```

3. **Запустите с Docker Compose**
```bash
# Убедитесь, что Docker Desktop запущен
./start-dev.sh
```

Или вручную:
```bash
docker-compose up --build
```

### Продакшен

```bash
./start-prod.sh
```

## 🐳 Docker команды

### Разработка
```bash
# Запуск всех сервисов
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Остановка
docker-compose down

# Пересборка
docker-compose up --build
```

### Продакшен
```bash
# Запуск продакшена
docker-compose -f docker-compose.prod.yml up -d

# Остановка
docker-compose -f docker-compose.prod.yml down

# Логи
docker-compose -f docker-compose.prod.yml logs -f
```

## 🚀 Деплой на Heroku

### 1. Подготовка

```bash
# Установите Heroku CLI
brew tap heroku/brew && brew install heroku

# Войдите в Heroku
heroku login

# Создайте приложение
heroku create your-app-name

# Добавьте PostgreSQL
heroku addons:create heroku-postgresql:mini
```

### 2. Настройка переменных

```bash
# Основные переменные
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set BOT_TOKEN="your-telegram-bot-token"
heroku config:set REACT_APP_API_URL="https://your-app-name.herokuapp.com"
```

### 3. Деплой

```bash
# Деплой на Heroku
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Инициализация базы данных
heroku run python backend/init_heroku_db.py

# Откройте приложение
heroku open
```

## 📁 Структура проекта

```
aeon_admin_hr-1/
├── backend/
│   ├── Dockerfile              # Docker образ для бэкенда
│   ├── requirements.txt        # Python зависимости
│   ├── init_heroku_db.py      # Инициализация БД для Heroku
│   └── app/                    # Код бэкенда
├── frontend/
│   ├── Dockerfile              # Docker образ для фронтенда
│   ├── package.json           # Node.js зависимости
│   └── src/                   # Код фронтенда
├── docker-compose.yml         # Локальная разработка
├── docker-compose.prod.yml    # Продакшен
├── heroku.yml                 # Конфигурация Heroku
├── nginx.conf                 # Nginx конфигурация
├── start-dev.sh              # Скрипт запуска для разработки
├── start-prod.sh             # Скрипт запуска для продакшена
└── env.example               # Пример переменных окружения
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` на основе `env.example`:

```env
# База данных
DATABASE_URL=postgresql://postgres:password@localhost:5432/hr_admin

# Безопасность
SECRET_KEY=your-secret-key-here

# Telegram Bot
BOT_TOKEN=your-telegram-bot-token

# Frontend API URL
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Тестирование

### API тесты
```bash
python3 test_api.py
```

### Docker тесты
```bash
# Проверка логов
docker-compose logs

# Подключение к контейнеру
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 📱 Telegram Mini Apps

### Настройка для Telegram

1. **Создайте бота через @BotFather**
2. **Настройте Web App URL**: `https://your-app-name.herokuapp.com`
3. **Добавьте BOT_TOKEN в переменные окружения**

### Использование

- Пользователи автоматически авторизуются через Telegram
- Первый пользователь становится администратором
- Администраторы могут добавлять других администраторов

## 🔍 Отладка

### Локальная разработка
```bash
# Логи всех сервисов
docker-compose logs

# Логи конкретного сервиса
docker-compose logs backend
docker-compose logs frontend
```

### Heroku
```bash
# Логи в реальном времени
heroku logs --tail

# Состояние приложения
heroku ps

# Консоль
heroku run bash
```

## 📚 Документация

- [Docker & Heroku Deploy](README_DOCKER.md)
- [Heroku Deploy Guide](HEROKU_DEPLOY.md)
- [Telegram Setup](TELEGRAM_SETUP.md)

## 🎉 Готово!

После деплоя ваше приложение будет доступно:
- **Локально**: `http://localhost:80`
- **Heroku**: `https://your-app-name.herokuapp.com`

### Проверка работы

1. **Откройте приложение**
2. **Проверьте API**: `/health`
3. **Протестируйте Telegram аутентификацию**

Приложение готово к использованию! 🚀 