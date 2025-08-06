# Aeon Admin HR System

Система управления HR-процессами с интеграцией Telegram и внешними API.

## 📁 Структура проекта

```
aeon_admin_hr-1/
├── backend/                 # Backend на FastAPI
│   ├── app/                # Основное приложение
│   │   ├── models.py       # Модели данных
│   │   ├── database.py     # Настройки базы данных
│   │   ├── routers/        # API роутеры
│   │   └── services/       # Бизнес-логика
│   ├── alembic/            # Миграции базы данных
│   ├── static/             # Статические файлы
│   ├── main.py             # Точка входа backend
│   ├── requirements.txt    # Python зависимости
│   └── Dockerfile          # Docker конфигурация
├── frontend/               # Frontend на React + TypeScript
│   ├── src/                # Исходный код
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы приложения
│   │   ├── hooks/          # React хуки
│   │   └── types/          # TypeScript типы
│   ├── public/             # Публичные файлы
│   ├── package.json        # Node.js зависимости
│   └── Dockerfile          # Docker конфигурация
├── docker-compose.yml      # Docker Compose конфигурация
├── render.yaml             # Конфигурация Render
├── main.py                 # Основной файл приложения
└── README.md               # Документация
```

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd aeon_admin_hr-1
   ```

2. **Настройте переменные окружения:**
   ```bash
   cp env.example .env
   cp backend/env.example backend/.env
   ```

3. **Запустите с помощью Docker:**
   ```bash
   ./start-full-docker.sh
   ```

4. **Или запустите локально:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python main.py
   
   # Frontend
   cd frontend
   npm install
   npm start
   ```

### Продакшн развертывание

1. **На Render:**
   ```bash
   ./deploy-render.sh
   ```

2. **С Docker:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 📚 Документация

- [Настройка Telegram авторизации](README_TELEGRAM_AUTH.md)
- [Настройка Docker](README_DOCKER.md)
- [Быстрый старт](QUICK_START.md)
- [Настройка системы](SETUP.md)
- [Настройка Cloudflare туннеля](CLOUDFLARE_TUNNEL_GUIDE.md)
- [Внешние API](EXTERNAL_API_GUIDE.md)
- [Уведомления Telegram](TELEGRAM_NOTIFICATIONS_GUIDE.md)

## 🛠 Основные скрипты

- `start-full-docker.sh` - Запуск полной системы в Docker
- `start-dev.sh` - Запуск для разработки
- `start-prod.sh` - Запуск продакшн версии
- `deploy-render.sh` - Развертывание на Render
- `build.sh` - Сборка проекта

## 🔧 Технологии

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **Frontend:** React, TypeScript, Tailwind CSS
- **Интеграции:** Telegram Bot API, Notion API
- **Развертывание:** Docker, Render, Cloudflare

## 📝 Лицензия

MIT License - см. файл [LICENSE](LICENSE) 