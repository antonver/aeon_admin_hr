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