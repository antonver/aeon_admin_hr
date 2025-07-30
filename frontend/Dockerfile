FROM node:18-alpine

WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Установка serve для продакшена
RUN npm install -g serve

# Открытие порта
EXPOSE 3000

# Команда запуска для продакшена
CMD ["serve", "-s", "build", "-l", "3000"] 