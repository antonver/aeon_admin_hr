# HR Admin Panel - Docker & Heroku Deploy

## 🐳 Быстрый старт с Docker

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

3. **Запустите приложение**
```bash
./start-dev.sh
```

Или вручную:
```bash
docker-compose up --build
```

### Продакшен

1. **Настройте переменные окружения**
```bash
cp env.example .env
# Отредактируйте .env файл для продакшена
```

2. **Запустите в продакшене**
```bash
./start-prod.sh
```

Или вручную:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🚀 Деплой на Heroku

### 1. Подготовка к деплою

1. **Установите Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Войдите в Heroku**
```bash
heroku login
```

3. **Создайте приложение на Heroku**
```bash
heroku create your-app-name
```

4. **Добавьте PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

### 2. Настройка переменных окружения

```bash
# Установите переменные окружения
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set BOT_TOKEN="your-telegram-bot-token"
heroku config:set REACT_APP_API_URL="https://your-app-name.herokuapp.com"
```

### 3. Деплой

```bash
# Деплой на Heroku
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 4. Инициализация базы данных

```bash
# Запустите миграцию базы данных
heroku run python backend/init_heroku_db.py
```

### 5. Откройте приложение

```bash
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

### Heroku переменные

```bash
# Получите DATABASE_URL автоматически
heroku config:get DATABASE_URL

# Установите остальные переменные
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set BOT_TOKEN="your-bot-token"
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

## 🔍 Отладка

### Проверка логов
```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx
```

### Подключение к контейнеру
```bash
# Бэкенд
docker-compose exec backend bash

# Фронтенд
docker-compose exec frontend sh

# База данных
docker-compose exec db psql -U postgres -d hr_admin
```

### Проверка состояния
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

## 🚀 Heroku команды

### Управление приложением
```bash
# Создание приложения
heroku create your-app-name

# Открытие приложения
heroku open

# Логи
heroku logs --tail

# Консоль
heroku run bash
```

### Переменные окружения
```bash
# Просмотр всех переменных
heroku config

# Установка переменной
heroku config:set KEY=value

# Удаление переменной
heroku config:unset KEY
```

### База данных
```bash
# Подключение к PostgreSQL
heroku pg:psql

# Резервное копирование
heroku pg:backups:capture

# Восстановление
heroku pg:backups:restore
```

## 🎯 Готово!

После деплоя ваше приложение будет доступно по адресу:
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Локально**: `http://localhost:80`

### Telegram Mini Apps

Для использования в Telegram Mini Apps:
1. Создайте бота через @BotFather
2. Настройте Web App URL: `https://your-app-name.herokuapp.com`
3. Добавьте BOT_TOKEN в переменные окружения Heroku

### Мониторинг

- **Heroku Dashboard**: https://dashboard.heroku.com/apps/your-app-name
- **Логи**: `heroku logs --tail`
- **Метрики**: Heroku Dashboard → Metrics

Приложение готово к использованию! 🚀 