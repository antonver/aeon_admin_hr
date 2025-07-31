# HR Admin System

Система управления HR-процессами с Telegram авторизацией и веб-интерфейсом.

## 🚀 Быстрый запуск

### 1. Установка зависимостей

```bash
# Установка Python зависимостей
cd backend
pip3 install -r requirements.txt

# Установка Node.js зависимостей
cd ../frontend
npm install
```

### 2. Настройка базы данных

```bash
# Переходим в папку backend
cd backend

# Создаем базу данных SQLite
export DATABASE_URL="sqlite:///./hr_admin.db"

# Инициализируем базу данных
python3 init_db.py

# Добавляем первого администратора (опционально)
python3 add_first_admin.py
```

### 3. Сборка фронтенда

```bash
# Переходим в папку frontend
cd ../frontend

# Собираем фронтенд для продакшена
npm run build

# Копируем собранные файлы в backend/static
cp -r build/* ../backend/static/
```

### 4. Запуск приложения

#### Вариант 1: Локальный запуск

```bash
# Запускаем бэкенд
cd backend
export DATABASE_URL="sqlite:///./hr_admin.db"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

Приложение будет доступно по адресу: http://localhost:8001

#### Вариант 2: Через Cloudflare Tunnel (для внешнего доступа)

```bash
# Запускаем бэкенд в фоне
cd backend
export DATABASE_URL="sqlite:///./hr_admin.db"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 &

# Запускаем Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8001
```

Приложение будет доступно по URL, который покажет Cloudflare Tunnel.

## 📁 Структура проекта

```
aeon_admin_hr-1/
├── backend/                 # Backend (FastAPI)
│   ├── app/                # Основной код приложения
│   │   ├── routers/        # API роутеры
│   │   ├── services/       # Бизнес-логика
│   │   └── models.py       # Модели базы данных
│   ├── static/             # Собранный фронтенд
│   ├── main.py             # Точка входа
│   └── requirements.txt    # Python зависимости
├── frontend/               # Frontend (React + TypeScript)
│   ├── src/               # Исходный код
│   ├── public/            # Статические файлы
│   └── package.json       # Node.js зависимости
└── README.md              # Этот файл
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в папке `backend`:

```env
DATABASE_URL=sqlite:///./hr_admin.db
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_WEBHOOK_URL=your_webhook_url
```

### Настройка Telegram бота

1. Создайте бота через @BotFather
2. Получите токен бота
3. Добавьте токен в переменные окружения
4. Настройте webhook (опционально)

## 🗄️ База данных

### SQLite (по умолчанию)

```bash
# Создание базы данных
cd backend
export DATABASE_URL="sqlite:///./hr_admin.db"
python3 init_db.py
```

### PostgreSQL (опционально)

```bash
# Установка PostgreSQL
brew install postgresql
brew services start postgresql

# Создание базы данных
createdb hr_admin_db

# Настройка переменной окружения
export DATABASE_URL="postgresql://username:password@localhost/hr_admin_db"
```

## 🚀 Разработка

### Запуск в режиме разработки

```bash
# Backend (с автоперезагрузкой)
cd backend
export DATABASE_URL="sqlite:///./hr_admin.db"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Frontend (в отдельном терминале)
cd frontend
npm start
```

### Миграции базы данных

```bash
cd backend
alembic upgrade head
```

## 📊 API Endpoints

### Основные эндпоинты

- `GET /api/health` - Проверка здоровья сервера
- `GET /api/telegram/profile` - Профиль пользователя
- `GET /api/candidates` - Список кандидатов
- `GET /api/metrics/overview` - Обзор метрик
- `POST /api/telegram/create-admin` - Создание администратора

### Документация API

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🔐 Авторизация

Система использует Telegram авторизацию:

1. Пользователь входит через Telegram
2. Получает JWT токен
3. Использует токен для доступа к API

## 🛠️ Устранение неполадок

### Проблема: "Error loading ASGI app"

```bash
# Убедитесь, что вы в правильной папке
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### Проблема: "address already in use"

```bash
# Найдите процесс, использующий порт
lsof -i :8001
# Остановите процесс
kill -9 <PID>
```

### Проблема: "unable to open database file"

```bash
# Проверьте права доступа к папке
ls -la backend/
# Создайте базу данных заново
cd backend
python3 init_db.py
```

### Проблема: "command not found: python"

```bash
# Используйте python3
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## 📝 Логи

### Backend логи

Логи сервера выводятся в консоль. Для продакшена рекомендуется настроить логирование в файл.

### Frontend логи

Логи React приложения выводятся в консоль браузера (F12 → Console).

## 🔄 Обновление приложения

### Обновление backend

```bash
cd backend
git pull
pip3 install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### Обновление frontend

```bash
cd frontend
git pull
npm install
npm run build
cp -r build/* ../backend/static/
```

## 📦 Docker (опционально)

### Сборка Docker образа

```bash
docker build -t hr-admin-backend ./backend
docker build -t hr-admin-frontend ./frontend
```

### Запуск через Docker Compose

```bash
docker-compose up -d
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License 