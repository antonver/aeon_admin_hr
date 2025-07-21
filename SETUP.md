# Настройка HR Admin Panel

## Быстрый запуск

1. **Клонируйте репозиторий**
   ```bash
   git clone <repository-url>
   cd aeon_admin_hr
   ```

2. **Запустите проект**
   ```bash
   ./start.sh
   ```

3. **Откройте в браузере**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## Настройка интеграций

### Telegram Bot

1. Создайте бота через @BotFather в Telegram
2. Получите токен бота
3. Добавьте бота в нужный чат
4. Получите ID чата (можно использовать @userinfobot)
5. Добавьте в `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

### Notion Integration

1. Создайте интеграцию в Notion:
   - Перейдите в https://www.notion.so/my-integrations
   - Создайте новую интеграцию
   - Скопируйте Internal Integration Token

2. Создайте базу данных кандидатов в Notion с полями:
   - Имя (Title)
   - Telegram (URL)
   - Email (Email)
   - Телефон (Phone)
   - Статус (Select: Ожидает, Прошёл, Приглашён, Отклонён)
   - Дата добавления (Date)
   - Последнее действие (Text)

3. Создайте базу данных задач с полями:
   - Название (Title)
   - Тип (Select)
   - Кандидат (Text)
   - Статус (Select)
   - Дата создания (Date)
   - Ссылка на кандидата (URL)

4. Добавьте в `.env`:
   ```
   NOTION_TOKEN=your_integration_token
   NOTION_DATABASE_ID=your_candidates_database_id
   NOTION_TASKS_DATABASE_ID=your_tasks_database_id
   ```

## Ручная установка (без Docker)

### Backend

1. **Установите Python 3.11+**
2. **Создайте виртуальное окружение**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных**
   ```bash
   # Для SQLite (по умолчанию)
   # Ничего не нужно делать
   
   # Для PostgreSQL
   # Установите PostgreSQL и создайте базу данных
   # Измените DATABASE_URL в .env
   ```

5. **Запустите сервер**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. **Установите Node.js 18+**
2. **Установите зависимости**
   ```bash
   cd frontend
   npm install
   ```

3. **Запустите приложение**
   ```bash
   npm start
   ```

## Структура проекта

```
aeon_admin_hr/
├── backend/                 # FastAPI сервер
│   ├── app/
│   │   ├── database.py     # Модели базы данных
│   │   ├── models.py       # Pydantic модели
│   │   ├── routers/        # API роутеры
│   │   └── services/       # Сервисы интеграций
│   ├── main.py             # Точка входа
│   └── requirements.txt    # Python зависимости
├── frontend/               # React приложение
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы приложения
│   │   └── App.tsx         # Главный компонент
│   └── package.json        # Node.js зависимости
├── docker-compose.yml      # Docker конфигурация
├── start.sh               # Скрипт запуска
└── README.md              # Документация
```

## API Endpoints

### Кандидаты
- `GET /api/candidates` - Список кандидатов
- `POST /api/candidates` - Создать кандидата
- `GET /api/candidates/{id}` - Получить кандидата
- `PUT /api/candidates/{id}` - Обновить кандидата
- `DELETE /api/candidates/{id}` - Удалить кандидата

### Интервью
- `GET /api/candidates/{id}/interview-logs` - Логи интервью
- `POST /api/candidates/{id}/interview-logs` - Добавить лог

### Комментарии
- `GET /api/candidates/{id}/comments` - Комментарии HR
- `POST /api/candidates/{id}/comments` - Добавить комментарий

### Быстрые действия
- `POST /api/candidates/{id}/quick-action` - Выполнить действие

### Метрики
- `GET /api/metrics/overview` - Общие метрики
- `GET /api/metrics/status-distribution` - Распределение по статусам
- `GET /api/metrics/activity-timeline` - Активность по дням
- `GET /api/metrics/interview-stats` - Статистика интервью
- `GET /api/metrics/top-candidates` - Топ кандидатов

### Уведомления
- `GET /api/notifications` - Список уведомлений
- `POST /api/notifications` - Создать уведомление
- `POST /api/notifications/send-test` - Тестовое уведомление

## Функциональность

### Основные возможности
- ✅ Управление кандидатами
- ✅ Отслеживание статусов
- ✅ Логи интервью ÆON
- ✅ Комментарии HR
- ✅ Быстрые действия
- ✅ Поиск и фильтрация
- ✅ Метрики и аналитика

### Интеграции
- ✅ Telegram Bot (уведомления, сообщения)
- ✅ Notion (автоматическая синхронизация)
- ✅ WebView для Telegram

### Быстрые действия
- ✅ Пригласить на тест
- ✅ Написать в Telegram
- ✅ Отправить фидбэк
- ✅ Скопировать данные

## Устранение неполадок

### Проблемы с Docker
```bash
# Пересобрать контейнеры
docker-compose down
docker-compose up --build

# Просмотр логов
docker-compose logs backend
docker-compose logs frontend
```

### Проблемы с базой данных
```bash
# Сброс базы данных
docker-compose down -v
docker-compose up
```

### Проблемы с интеграциями
1. Проверьте токены в `.env`
2. Убедитесь, что бот добавлен в чат
3. Проверьте права интеграции в Notion

## Разработка

### Добавление новых функций
1. Создайте модель в `backend/app/database.py`
2. Добавьте Pydantic модель в `backend/app/models.py`
3. Создайте роутер в `backend/app/routers/`
4. Добавьте компонент в `frontend/src/components/`
5. Создайте страницу в `frontend/src/pages/`

### Тестирование
```bash
# Backend тесты
cd backend
python -m pytest

# Frontend тесты
cd frontend
npm test
```

## Лицензия

MIT License 