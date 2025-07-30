FROM node:18-alpine

WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода
COPY . .

# Установка прав доступа для node_modules
RUN chmod +x node_modules/.bin/*

# Открытие порта
EXPOSE 3000

# Команда запуска
CMD ["npm", "start"] 