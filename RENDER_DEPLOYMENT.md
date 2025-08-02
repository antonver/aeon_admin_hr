# Деплой на Render

Это руководство поможет вам развернуть HR Admin Panel на платформе Render.

## Предварительные требования

1. Аккаунт на [Render.com](https://render.com)
2. Telegram Bot Token
3. Notion API Token (опционально)
4. Git репозиторий с кодом

## Шаги деплоя

### 1. Подготовка репозитория

Убедитесь, что ваш код находится в Git репозитории и содержит все необходимые файлы:

- `render.yaml` - конфигурация Render
- `build.sh` - скрипт сборки
- `start.sh` - скрипт запуска
- `backend/requirements.txt` - Python зависимости
- `frontend/package.json` - Node.js зависимости

### 2. Создание сервисов на Render

#### Вариант A: Автоматический деплой через render.yaml

1. Зайдите в [Render Dashboard](https://dashboard.render.com)
2. Нажмите "New +" → "Blueprint"
3. Подключите ваш Git репозиторий
4. Выберите файл `render.yaml`
5. Render автоматически создаст все сервисы

#### Вариант B: Ручное создание сервисов

##### 2.1 Создание базы данных PostgreSQL

1. "New +" → "PostgreSQL"
2. Название: `hr-admin-db`
3. План: Free
4. Нажмите "Create Database"

##### 2.2 Создание бэкенд сервиса

1. "New +" → "Web Service"
2. Подключите Git репозиторий
3. Настройки:
   - **Name**: `hr-admin-backend`
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`
   - **Plan**: Free

4. Переменные окружения:
   ```
   DATABASE_URL = [из базы данных]
   SECRET_KEY = [сгенерировать]
   BOT_TOKEN = [ваш Telegram Bot Token]
   NOTION_TOKEN = [ваш Notion Token]
   NOTION_DATABASE_ID = [ваш Notion Database ID]
   PYTHON_VERSION = 3.11.0
   ```

##### 2.3 Создание фронтенд сервиса

1. "New +" → "Static Site"
2. Подключите Git репозиторий
3. Настройки:
   - **Name**: `hr-admin-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Plan**: Free

4. Переменные окружения:
   ```
   REACT_APP_API_URL = https://hr-admin-backend.onrender.com
   REACT_APP_TELEGRAM_BOT_USERNAME = [ваш бот username]
   ```

### 3. Настройка переменных окружения

#### Обязательные переменные:

- `DATABASE_URL` - автоматически настроится Render
- `SECRET_KEY` - сгенерируйте случайную строку
- `BOT_TOKEN` - токен вашего Telegram бота

#### Опциональные переменные:

- `NOTION_TOKEN` - для интеграции с Notion
- `NOTION_DATABASE_ID` - ID базы данных Notion
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений

### 4. Получение Telegram Bot Token

1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен

### 5. Настройка Notion (опционально)

1. Создайте интеграцию на [notion.so/my-integrations](https://notion.so/my-integrations)
2. Получите токен
3. Добавьте интеграцию в вашу базу данных
4. Скопируйте ID базы данных из URL

### 6. Проверка деплоя

После успешного деплоя:

1. Проверьте бэкенд: `https://hr-admin-backend.onrender.com/health`
2. Проверьте фронтенд: `https://hr-admin-frontend.onrender.com`
3. Проверьте API документацию: `https://hr-admin-backend.onrender.com/docs`

## Структура URL после деплоя

- **Frontend**: `https://hr-admin-frontend.onrender.com`
- **Backend API**: `https://hr-admin-backend.onrender.com`
- **API Docs**: `https://hr-admin-backend.onrender.com/docs`
- **Health Check**: `https://hr-admin-backend.onrender.com/health`

## Мониторинг и логи

- Логи доступны в Render Dashboard для каждого сервиса
- Health checks автоматически проверяют доступность сервисов
- Render отправляет уведомления о проблемах

## Обновление приложения

Для обновления приложения просто запушьте изменения в Git репозиторий. Render автоматически пересоберет и перезапустит сервисы.

## Устранение неполадок

### Проблемы с базой данных
- Проверьте переменную `DATABASE_URL`
- Убедитесь, что база данных создана и доступна

### Проблемы с бэкендом
- Проверьте логи в Render Dashboard
- Убедитесь, что все переменные окружения настроены
- Проверьте health check endpoint

### Проблемы с фронтендом
- Проверьте переменную `REACT_APP_API_URL`
- Убедитесь, что бэкенд доступен
- Проверьте логи сборки

## Поддержка

Если у вас возникли проблемы:

1. Проверьте логи в Render Dashboard
2. Убедитесь, что все переменные окружения настроены правильно
3. Проверьте, что все зависимости указаны в requirements.txt и package.json
4. Обратитесь в поддержку Render или создайте issue в репозитории 