# 🔧 Исправление проблемы Docker BuildKit

## Проблема
При сборке Docker образа для frontend возникала ошибка:
```
failed to solve: failed to prepare extraction snapshot "extract-295166583-1sbW sha256:8e39517323a1e78fd800ad62b3849156794c907f54fda8b78c22a6ddb6c8d60a": parent snapshot sha256:6728f3943687a2e09f3b717e279e445af8f4a93fd3f5ad135cb8865ec6dc5586 does not exist: not found
```

## Причина
Проблема была связана с:
1. Неоптимальной структурой Dockerfile для frontend
2. Проблемами кэширования слоев в Docker BuildKit
3. Неправильной конфигурацией docker-compose.yml для production сборки

## Решение

### 1. Оптимизация Dockerfile для frontend
Изменили `frontend/Dockerfile` на multi-stage build:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./

# Установка всех зависимостей (включая devDependencies для сборки)
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Продакшен образ
FROM node:18-alpine AS production

WORKDIR /app

# Установка serve глобально
RUN npm install -g serve

# Копирование собранного приложения из builder
COPY --from=builder /app/build ./build

# Открытие порта
EXPOSE 3000

# Команда запуска для продакшена
CMD ["serve", "-s", "build", "-l", "3000"]
```

### 2. Обновление docker-compose.yml
Изменили конфигурацию frontend:

```yaml
frontend:
  build: 
    context: ./frontend
    target: production
  environment:
    - REACT_APP_API_URL=http://localhost:8000
  ports:
    - "3002:3000"
  depends_on:
    - backend
```

### 3. Очистка Docker кэша
```bash
docker system prune -f
docker-compose build --no-cache
```

### 4. Удаление устаревшей версии
Убрали устаревшую строку `version: '3.8'` из docker-compose.yml.

## Результат
✅ Все контейнеры успешно собираются и запускаются
✅ Frontend работает в production режиме с serve
✅ Backend API доступен на порту 8000
✅ База данных PostgreSQL работает корректно
✅ Nginx проксирует запросы

## Доступ к системе
- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **База данных**: localhost:5432

## Команды для управления
```bash
# Запуск системы
docker-compose up -d

# Остановка системы
docker-compose down

# Просмотр логов
docker-compose logs -f

# Пересборка образов
docker-compose build --no-cache
``` 