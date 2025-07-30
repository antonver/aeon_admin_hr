# Настройка Telegram Mini Apps аутентификации

## Обзор изменений

Реализована аутентификация через Telegram Mini Apps с следующими возможностями:

1. **Бесшовная аутентификация** - пользователи автоматически авторизуются через Telegram
2. **Автоматическое назначение первого пользователя администратором**
3. **Управление администраторами** - возможность добавлять новых админов по username
4. **Убрана панель уведомлений** со всех страниц

## Структура изменений

### Бэкенд

1. **Обновлена модель User** (`backend/app/database.py`):
   - Добавлены поля: `telegram_id`, `telegram_username`, `is_admin`
   - Поля `email` и `password` стали опциональными

2. **Новый роутер** (`backend/app/routers/telegram_auth.py`):
   - `/api/telegram/telegram-auth` - аутентификация через Telegram
   - `/api/telegram/profile` - получение профиля пользователя
   - `/api/telegram/create-admin` - создание нового администратора
   - `/api/telegram/admins` - список всех администраторов

3. **Валидация init_data** от Telegram Mini Apps

### Фронтенд

1. **Новый хук** (`frontend/src/hooks/useTelegramAuth.ts`):
   - Автоматическая аутентификация через Telegram SDK
   - Управление состоянием пользователя и токена

2. **Обновлен Layout** (`frontend/src/components/Layout.tsx`):
   - Убрана панель уведомлений
   - Интегрирована Telegram аутентификация
   - Добавлен пункт "Администраторы" для админов

3. **Новая страница** (`frontend/src/pages/Admins.tsx`):
   - Управление администраторами
   - Добавление новых админов по username

## Настройка

### 1. Переменные окружения

Добавьте в `.env` файл:

```env
BOT_TOKEN=your_telegram_bot_token
SECRET_KEY=your_jwt_secret_key
```

### 2. Создание Telegram бота

1. Создайте бота через @BotFather в Telegram
2. Получите токен бота
3. Настройте Web App для бота

### 3. Запуск

```bash
# Бэкенд
cd backend
python3 main.py

# Фронтенд
cd frontend
npm start
```

## Использование

### Для разработки

1. Откройте `test_telegram_auth.html` в браузере
2. Используйте Telegram Web App для тестирования аутентификации

### Для продакшена

1. Разместите фронтенд на HTTPS домене
2. Настройте Telegram Web App URL в настройках бота
3. Убедитесь, что BOT_TOKEN настроен правильно

## API Endpoints

### Аутентификация
```http
POST /api/telegram/telegram-auth
Content-Type: application/json

{
  "init_data": "telegram_init_data_string"
}
```

### Профиль пользователя
```http
GET /api/telegram/profile
Authorization: Bearer <token>
```

### Создание администратора
```http
POST /api/telegram/create-admin
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "telegram_username": "username"
}
```

### Список администраторов
```http
GET /api/telegram/admins
Authorization: Bearer <admin_token>
```

## Логика работы

1. **Первый пользователь** автоматически становится администратором
2. **Последующие пользователи** создаются как обычные пользователи
3. **Администраторы** могут добавлять других пользователей как администраторов
4. **Аутентификация** происходит автоматически при открытии приложения в Telegram

## Безопасность

- Валидация `init_data` от Telegram
- JWT токены для аутентификации
- Проверка прав доступа для административных функций
- Хеширование паролей (для совместимости со старой системой) 