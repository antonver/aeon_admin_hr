#!/bin/bash

# Скрипт сборки для Render
echo "🚀 Начинаем сборку проекта..."

# Устанавливаем зависимости Python
echo "📦 Устанавливаем Python зависимости..."
pip install -r backend/requirements.txt

# Создаем необходимые директории
echo "📁 Создаем директории..."
mkdir -p backend/static

# Копируем статические файлы фронтенда в бэкенд (фронтенд уже собран в render.yaml)
echo "📋 Копируем статические файлы фронтенда..."
if [ -d "frontend/build" ]; then
    echo "🧹 Очищаем старые статические файлы..."
    rm -rf backend/static/*
    echo "📋 Копируем новые статические файлы..."
    cp -r frontend/build/* backend/static/
    
    # ПРИНУДИТЕЛЬНО исправляем структуру папок - перемещаем файлы из static/static/ в static/
    if [ -d "backend/static/static" ]; then
        echo "🔧 Исправляем структуру папок (static/static/ -> static/)..."
        # Перемещаем CSS файлы
        if [ -d "backend/static/static/css" ]; then
            mkdir -p backend/static/css
            mv backend/static/static/css/* backend/static/css/ 2>/dev/null || true
        fi
        # Перемещаем JS файлы  
        if [ -d "backend/static/static/js" ]; then
            mkdir -p backend/static/js
            mv backend/static/static/js/* backend/static/js/ 2>/dev/null || true
        fi
        # Удаляем пустые директории
        rmdir backend/static/static/css 2>/dev/null || true
        rmdir backend/static/static/js 2>/dev/null || true
        rmdir backend/static/static 2>/dev/null || true
        echo "✅ Структура папок исправлена"
    fi
    
    echo "✅ Статические файлы обновлены"
    echo "📁 Проверяем структуру файлов:"
    ls -la backend/static/
    ls -la backend/static/js/ 2>/dev/null || echo "⚠️  JS файлы не найдены"
    ls -la backend/static/css/ 2>/dev/null || echo "⚠️  CSS файлы не найдены"
    
    # Проверяем что index.html содержит правильные пути
    echo "📄 Проверяем index.html..."
    if ls backend/static/js/main.*.js 1> /dev/null 2>&1; then
        echo "✅ JS файлы найдены в правильной директории"
    else
        echo "❌ JS файлы не найдены"
    fi
    
    if ls backend/static/css/main.*.css 1> /dev/null 2>&1; then
        echo "✅ CSS файлы найдены в правильной директории"
    else
        echo "❌ CSS файлы не найдены"
    fi
else
    echo "⚠️  Директория frontend/build не найдена"
    mkdir -p backend/static
fi

# Инициализируем базу данных
echo "🗄️  Инициализируем базу данных..."
cd backend
python init_heroku_db.py

echo "✅ Сборка завершена!" 