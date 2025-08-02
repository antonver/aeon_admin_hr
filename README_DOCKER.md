# 🐳 HR Admin System - Docker версия

## 🚀 Быстрый запуск

### Полный запуск с Docker и Cloudflare Tunnel
```bash
./start-full-docker.sh
```

### Запуск только с Docker (без туннеля)
```bash
./start-docker-only.sh
```

### Остановка системы
```bash
./stop-full-docker.sh
```

## 📋 Требования

- Docker Desktop
- Docker Compose
- cloudflared (устанавливается автоматически)

## 🏗️ Архитектура

Система состоит из следующих контейнеров:

### 1. База данных (PostgreSQL)
- **Образ**: `postgres:15-alpine`
- **Порт**: `5432`
- **База данных**: `hr_admin`
- **Пользователь**: `postgres`
- **Пароль**: `password`

### 2. Backend API (FastAPI)
- **Образ**: Собирается из `./backend/Dockerfile`
- **Порт**: `8000`
- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **Автоинициализация**: Создает таблицы и тестовые данные

### 3. Frontend (React)
- **Образ**: Собирается из `./frontend/Dockerfile`
- **Порт**: `3000`
- **Фреймворк**: React + TypeScript
- **API**: Подключается к backend на порту 8000

### 4. Nginx (Прокси)
- **Образ**: `nginx:alpine`
- **Порт**: `80`
- **Назначение**: Проксирование запросов к frontend и backend

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# База данных
DATABASE_URL=postgresql://postgres:password@db:5432/hr_admin

# Безопасность
SECRET_KEY=your-secret-key-here

# Telegram Bot
BOT_TOKEN=your-telegram-bot-token

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Cloudflare Tunnel

Для настройки Cloudflare Tunnel:

1. Создайте туннель в Cloudflare Dashboard
2. Скачайте credentials файл
3. Поместите его в `.cloudflared/credentials.json`
4. Отредактируйте `cloudflared.yml`:

```yaml
tunnel: your-tunnel-name
credentials-file: .cloudflared/credentials.json
ingress:
  - hostname: your-domain.com
    service: http://localhost:8000
  - service: http_status:404
```

## 📊 Доступ к системе

### Локальный доступ
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Проверка здоровья**: http://localhost:8000/api/health

### Внешний доступ
- **Прямой IP**: http://YOUR_IP:8000 (если порт открыт)
- **Cloudflare Tunnel**: https://your-domain.com (если настроен)

### База данных
- **Host**: localhost
- **Port**: 5432
- **Database**: hr_admin
- **Username**: postgres
- **Password**: password

## 🛠️ Управление

### Основные команды

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Просмотр статуса
docker-compose ps

# Перезапуск сервиса
docker-compose restart backend

# Пересборка образов
docker-compose build --no-cache
```

### Отдельные сервисы

```bash
# Только база данных
docker-compose up -d db

# Только backend
docker-compose up -d backend

# Только frontend
docker-compose up -d frontend
```

## 🔍 Отладка

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Последние 100 строк
docker-compose logs --tail=100 backend
```

### Подключение к контейнерам

```bash
# Backend контейнер
docker-compose exec backend bash

# База данных
docker-compose exec db psql -U postgres -d hr_admin

# Frontend контейнер
docker-compose exec frontend sh
```

### Проверка здоровья

```bash
# API
curl http://localhost:8000/api/health

# База данных
docker-compose exec db pg_isready -U postgres

# Frontend
curl http://localhost:3000
```

## 🗄️ База данных

### Инициализация

База данных автоматически инициализируется при первом запуске:

1. Создаются все таблицы
2. Создается тестовый админ:
   - Email: `admin@example.com`
   - Пароль: `admin123`
3. Добавляются тестовые кандидаты

### Ручная инициализация

```bash
# Подключение к backend контейнеру
docker-compose exec backend bash

# Инициализация БД
python init_heroku_db.py

# Добавление тестовых данных
python seed_test_data.py
```

### Резервное копирование

```bash
# Создание бэкапа
docker-compose exec db pg_dump -U postgres hr_admin > backup.sql

# Восстановление
docker-compose exec -T db psql -U postgres hr_admin < backup.sql
```

## 🔒 Безопасность

### Рекомендации для продакшена

1. **Измените пароли по умолчанию**
2. **Используйте сильный SECRET_KEY**
3. **Настройте SSL/TLS**
4. **Ограничьте доступ к базе данных**
5. **Регулярно обновляйте образы**

### Переменные окружения для продакшена

```env
DATABASE_URL=postgresql://user:strong_password@db:5432/hr_admin
SECRET_KEY=very-long-random-secret-key
BOT_TOKEN=your-telegram-bot-token
NODE_ENV=production
```

## 🚨 Устранение неполадок

### Проблема: "Port already in use"
```bash
# Найдите процесс
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Остановите процесс
kill -9 <PID>
```

### Проблема: "Database connection failed"
```bash
# Проверьте статус БД
docker-compose logs db

# Перезапустите БД
docker-compose restart db
```

### Проблема: "Build failed"
```bash
# Очистите кэш
docker system prune -a

# Пересоберите образы
docker-compose build --no-cache
```

### Проблема: "Permission denied"
```bash
# Исправьте права доступа
sudo chown -R $USER:$USER .

# Перезапустите Docker
sudo systemctl restart docker
```

## 📚 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что все порты свободны
3. Проверьте, что Docker запущен
4. Обратитесь к разделу "Устранение неполадок" 