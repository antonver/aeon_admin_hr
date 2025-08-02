# 🔄 Инструкции по обновлению Heroku

## Для вашего друга (владельца Heroku приложения)

### 1. Добавить вас как collaborator

```bash
# Войдите в аккаунт Heroku вашего друга
heroku login

# Добавьте доступ для anton.verbovyi@gmail.com
heroku access:add anton.verbovyi@gmail.com --app aeon-hr-admin
```

### 2. Обновить приложение

После того как вы получите доступ, выполните:

```bash
# Клонируйте репозиторий (если еще не клонирован)
git clone https://github.com/antonver/aeon_admin_hr.git
cd aeon_admin_hr

# Добавьте remote для Heroku
git remote add heroku https://git.heroku.com/aeon-hr-admin.git

# Получите последние изменения
git pull origin main

# Запушьте на Heroku
git push heroku main

# Запустите миграции базы данных
heroku run python backend/init_heroku_db.py --app aeon-hr-admin
```

### 3. Проверить статус

```bash
# Проверить логи
heroku logs --tail --app aeon-hr-admin

# Проверить статус приложения
heroku ps --app aeon-hr-admin
```

## Для вас (после получения доступа)

### 1. Получить доступ к приложению

```bash
# Войдите в свой аккаунт Heroku
heroku login

# Проверьте доступные приложения
heroku apps
```

### 2. Обновить приложение

```bash
# Запушьте изменения
git push heroku main

# Запустите миграции
heroku run python backend/init_heroku_db.py --app aeon-hr-admin
```

### 3. Проверить обновление

```bash
# Откройте приложение
heroku open --app aeon-hr-admin

# Проверьте логи
heroku logs --tail --app aeon-hr-admin
```

## Альтернатива: Деплой на Render

Если у вас нет доступа к Heroku, можете развернуть на Render:

```bash
# Запустите скрипт деплоя
./deploy-render.sh
```

Затем следуйте инструкциям в `RENDER_DEPLOYMENT.md`

## Полезные команды Heroku

```bash
# Просмотр переменных окружения
heroku config --app aeon-hr-admin

# Установка переменной окружения
heroku config:set BOT_TOKEN=your_token --app aeon-hr-admin

# Перезапуск приложения
heroku restart --app aeon-hr-admin

# Просмотр метрик
heroku addons:open papertrail --app aeon-hr-admin
```

## Устранение проблем

### Если приложение не обновляется:

1. Проверьте логи: `heroku logs --tail --app aeon-hr-admin`
2. Перезапустите приложение: `heroku restart --app aeon-hr-admin`
3. Проверьте переменные окружения: `heroku config --app aeon-hr-admin`

### Если база данных не обновляется:

```bash
# Запустите миграции вручную
heroku run python backend/init_heroku_db.py --app aeon-hr-admin

# Или через Alembic
heroku run alembic upgrade head --app aeon-hr-admin
``` 