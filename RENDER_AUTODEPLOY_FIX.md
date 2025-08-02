# 🔧 Решение проблем с автодеплоем на Render

## 📋 Проблема
У вас установлен Render CLI, но автодеплой не работает из-за неправильной конфигурации существующего сервиса.

## 🔍 Диагностика

### ✅ Что работает:
- ✅ Render CLI установлен и авторизован
- ✅ Сервис `aeon_admin_hr` существует
- ✅ Зависимости устанавливаются корректно
- ✅ Код обновлен в GitHub

### ❌ Проблемы найдены:
- ❌ **Build Command:** `pip install -r requirements.txt` (должно быть `./build.sh`)
- ❌ **Start Command:** `gunicorn app:app` (должно быть `./start.sh`)
- ❌ **Отсутствуют переменные окружения** (BOT_TOKEN и др.)

## 🛠️ Решение

### Шаг 1: Обновите настройки сервиса

1. **Откройте Dashboard:** https://dashboard.render.com/web/srv-d272anh5pdvs73c1hdpg
2. **Перейдите в раздел "Settings"**
3. **Обновите настройки:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `./start.sh`
4. **Добавьте переменные окружения:**
   - `BOT_TOKEN` (обязательно) - токен вашего Telegram бота
   - `NOTION_TOKEN` (опционально)
   - `NOTION_DATABASE_ID` (опционально)
5. **Нажмите "Save Changes"**

### Шаг 2: Запустите новый деплой

1. **Перейдите в раздел "Manual Deploy"**
2. **Нажмите "Deploy latest commit"**
3. **Дождитесь завершения деплоя**

## 🚀 Альтернативные решения

### Вариант 1: Создать новый Blueprint (рекомендуется)

1. **Удалите старый сервис** через dashboard
2. **Создайте новый Blueprint:**
   - Нажмите "New +" → "Blueprint"
   - Подключите репозиторий: `https://github.com/antonver/aeon_admin_hr.git`
   - Выберите файл `render.yaml`
   - Нажмите "Apply"

### Вариант 2: Использовать CLI для мониторинга

```bash
# Проверить статус сервиса
render services

# Посмотреть логи
render logs -r srv-d272anh5pdvs73c1hdpg --tail

# Перезапустить сервис
render restart srv-d272anh5pdvs73c1hdpg
```

## 📊 Полезные команды

### Диагностика:
```bash
# Проверить готовность проекта
python3 check-render-readiness.py

# Диагностика проблем с деплоем
./fix-render-deploy.sh

# Проверить авторизацию
render whoami
```

### Мониторинг:
```bash
# Логи в реальном времени
render logs -r srv-d272anh5pdvs73c1hdpg --tail

# Статус сервисов
render services --output json

# Health check
curl https://aeon-admin-hr.onrender.com/health
```

## 🔧 Исправленные файлы

### ✅ Обновленные конфигурации:
- **`render.yaml`** - добавлен `autoDeploy: true` и `branch: main`
- **`build.sh`** - улучшена сборка фронтенда
- **`start.sh`** - правильная команда запуска

### ✅ Новые скрипты:
- **`fix-render-deploy.sh`** - диагностика и исправление проблем
- **`deploy-render-cli.sh`** - автоматический деплой через CLI

## 📝 Пошаговое решение

### Быстрое исправление:
```bash
# 1. Запустите диагностику
./fix-render-deploy.sh

# 2. Следуйте инструкциям на экране
# 3. Обновите настройки в dashboard
# 4. Запустите новый деплой
```

### Полное решение:
```bash
# 1. Проверьте готовность
python3 check-render-readiness.py

# 2. Запустите диагностику
./fix-render-deploy.sh

# 3. Обновите настройки в dashboard
# 4. Добавьте переменные окружения
# 5. Запустите деплой
# 6. Проверьте логи
render logs -r srv-d272anh5pdvs73c1hdpg --tail
```

## 🌐 После исправления

### URL структура:
- **Backend:** https://aeon-admin-hr.onrender.com
- **API Docs:** https://aeon-admin-hr.onrender.com/docs
- **Health Check:** https://aeon-admin-hr.onrender.com/health

### Автодеплой:
- ✅ Автоматический деплой при push в main ветку
- ✅ Автоматическая пересборка при изменениях
- ✅ Health checks для мониторинга

## 📞 Поддержка

Если проблемы остаются:
1. **Проверьте логи:** `render logs -r srv-d272anh5pdvs73c1hdpg --tail`
2. **Перезапустите сервис:** `render restart srv-d272anh5pdvs73c1hdpg`
3. **Создайте новый Blueprint** с `render.yaml`
4. **Обратитесь в поддержку Render**

---

**Статус:** 🔧 Проблемы диагностированы и готовы к исправлению! 