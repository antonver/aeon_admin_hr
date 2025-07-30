# 🚀 Деплой на Heroku

## Подготовка к деплою

### 1. Установка Heroku CLI

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Ubuntu/Debian:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Windows:**
Скачайте установщик с [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### 2. Вход в Heroku

```bash
heroku login
```

### 3. Создание приложения

```bash
# Создайте новое приложение
heroku create your-app-name

# Или используйте существующее
heroku git:remote -a your-app-name
```

### 4. Добавление PostgreSQL

```bash
# Добавьте PostgreSQL addon
heroku addons:create heroku-postgresql:mini
```

## Настройка переменных окружения

### 1. Основные переменные

```bash
# Безопасность
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Telegram Bot (если есть)
heroku config:set BOT_TOKEN="your-telegram-bot-token"

# Frontend API URL
heroku config:set REACT_APP_API_URL="https://your-app-name.herokuapp.com"
```

### 2. Проверка переменных

```bash
# Посмотреть все переменные
heroku config

# Получить DATABASE_URL
heroku config:get DATABASE_URL
```

## Деплой приложения

### 1. Подготовка Git

```bash
# Добавьте все файлы
git add .

# Создайте коммит
git commit -m "Deploy to Heroku"

# Убедитесь, что у вас есть remote для Heroku
git remote -v
```

### 2. Деплой

```bash
# Деплой на Heroku
git push heroku main

# Если используете master ветку
git push heroku master
```

### 3. Инициализация базы данных

```bash
# Запустите миграцию базы данных
heroku run python backend/init_heroku_db.py
```

### 4. Откройте приложение

```bash
heroku open
```

## Проверка деплоя

### 1. Логи

```bash
# Посмотреть логи в реальном времени
heroku logs --tail

# Посмотреть последние логи
heroku logs
```

### 2. Состояние приложения

```bash
# Проверить статус
heroku ps

# Перезапустить приложение
heroku restart
```

### 3. Консоль

```bash
# Подключиться к консоли
heroku run bash

# Выполнить команду
heroku run python backend/test_api.py
```

## Настройка для Telegram Mini Apps

### 1. Создание бота

1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните токен бота

### 2. Настройка Web App

1. Отправьте `/mybots` @BotFather
2. Выберите ваш бота
3. Нажмите "Bot Settings" → "Menu Button"
4. Установите URL: `https://your-app-name.herokuapp.com`

### 3. Настройка переменных

```bash
# Добавьте токен бота
heroku config:set BOT_TOKEN="your-bot-token-here"
```

## Мониторинг и обслуживание

### 1. Heroku Dashboard

- Откройте [dashboard.heroku.com](https://dashboard.heroku.com)
- Выберите ваше приложение
- Мониторьте метрики и логи

### 2. База данных

```bash
# Подключение к PostgreSQL
heroku pg:psql

# Резервное копирование
heroku pg:backups:capture

# Список бэкапов
heroku pg:backups

# Восстановление
heroku pg:backups:restore b001 DATABASE_URL
```

### 3. Масштабирование

```bash
# Увеличить количество dynos
heroku ps:scale web=2

# Уменьшить
heroku ps:scale web=1
```

## Устранение неполадок

### 1. Проблемы с деплоем

```bash
# Проверить логи сборки
heroku logs --tail

# Пересобрать приложение
git commit --allow-empty -m "Redeploy"
git push heroku main
```

### 2. Проблемы с базой данных

```bash
# Проверить подключение к БД
heroku pg:info

# Сбросить базу данных
heroku pg:reset DATABASE_URL
heroku run python backend/init_heroku_db.py
```

### 3. Проблемы с переменными окружения

```bash
# Проверить все переменные
heroku config

# Удалить переменную
heroku config:unset VARIABLE_NAME

# Установить переменную
heroku config:set VARIABLE_NAME=value
```

## Полезные команды

### Управление приложением

```bash
# Открыть приложение
heroku open

# Перезапустить
heroku restart

# Остановить
heroku ps:scale web=0

# Запустить
heroku ps:scale web=1
```

### Работа с Git

```bash
# Добавить remote
heroku git:remote -a your-app-name

# Удалить remote
git remote remove heroku

# Проверить remotes
git remote -v
```

### Переменные окружения

```bash
# Установить переменную
heroku config:set KEY=value

# Получить переменную
heroku config:get KEY

# Удалить переменную
heroku config:unset KEY
```

## 🎉 Готово!

После успешного деплоя ваше приложение будет доступно по адресу:
`https://your-app-name.herokuapp.com`

### Проверка работы

1. **Откройте приложение**: `heroku open`
2. **Проверьте API**: `https://your-app-name.herokuapp.com/health`
3. **Проверьте логи**: `heroku logs --tail`

### Telegram Mini Apps

Для использования в Telegram:
1. Создайте бота через @BotFather
2. Настройте Web App URL в настройках бота
3. Добавьте BOT_TOKEN в переменные окружения
4. Протестируйте аутентификацию в Telegram

Приложение готово к использованию! 🚀 