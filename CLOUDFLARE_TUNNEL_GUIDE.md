# 🌐 Настройка Cloudflare Tunnel

## ✅ Быстрый запуск

### Автоматическая настройка
```bash
./start-cloudflare-simple.sh
```

### Ручная настройка
```bash
# Запуск туннеля для backend API
cloudflared tunnel --url http://localhost:8000

# Запуск туннеля для frontend
cloudflared tunnel --url http://localhost:3002
```

## 🔧 Управление туннелями

### Запуск
```bash
./start-cloudflare-simple.sh
```

### Остановка
```bash
./stop-cloudflare.sh
```

### Проверка статуса
```bash
# Проверка процессов
ps aux | grep cloudflared

# Просмотр логов
tail -f cloudflared-backend.log
tail -f cloudflared-frontend.log
```

## 📋 Текущие URL туннелей

### Backend API
- **URL**: https://lighting-however-refer-endless.trycloudflare.com
- **Статус**: ✅ Работает
- **Проверка**: `curl https://lighting-however-refer-endless.trycloudflare.com/api/health`

### Frontend
- **URL**: https://manual-everyone-concentration-heat.trycloudflare.com
- **Статус**: ✅ Работает
- **Проверка**: `curl https://manual-everyone-concentration-heat.trycloudflare.com`

## 🚀 Интеграция с основным скриптом

Основной скрипт `./start-full-docker.sh` теперь автоматически:
1. Запускает Docker сервисы
2. Настраивает Cloudflare Tunnel
3. Показывает URL для внешнего доступа

## 🔍 Отладка

### Проблема: "Туннель не запускается"
```bash
# Проверка установки cloudflared
which cloudflared

# Переустановка
brew install cloudflare/cloudflare/cloudflared
```

### Проблема: "URL не отображается"
```bash
# Проверка логов
tail -f cloudflared-backend.log
tail -f cloudflared-frontend.log

# Перезапуск туннелей
./stop-cloudflare.sh
./start-cloudflare-simple.sh
```

### Проблема: "Ошибка подключения"
```bash
# Проверка локальных сервисов
curl http://localhost:8000/api/health
curl http://localhost:3002

# Перезапуск Docker сервисов
docker-compose restart
```

## 📊 Мониторинг

### Логи туннелей
```bash
# Backend API
tail -f cloudflared-backend.log

# Frontend
tail -f cloudflared-frontend.log
```

### Статус процессов
```bash
ps aux | grep cloudflared
```

### Проверка доступности
```bash
# Backend API
curl -s https://lighting-however-refer-endless.trycloudflare.com/api/health

# Frontend
curl -s https://manual-everyone-concentration-heat.trycloudflare.com
```

## 🎯 Преимущества

✅ **Автоматическая настройка** - не требует ручной конфигурации
✅ **Быстрый доступ** - мгновенное получение публичных URL
✅ **Безопасность** - HTTPS шифрование
✅ **Простота** - один скрипт для запуска/остановки
✅ **Мониторинг** - подробные логи и статус

## 🔄 Обновление URL

URL туннелей могут изменяться при перезапуске. Для получения актуальных URL:

```bash
# Автоматическое получение
./start-cloudflare-simple.sh

# Ручное получение из логов
grep -o "https://.*trycloudflare.com" cloudflared-backend.log
grep -o "https://.*trycloudflare.com" cloudflared-frontend.log
``` 