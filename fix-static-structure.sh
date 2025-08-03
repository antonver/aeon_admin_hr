#!/bin/bash

echo "🔧 Автоматическое исправление структуры статических файлов..."

# Проверяем и исправляем проблемную структуру
if [ -d "backend/static/static" ]; then
    echo "❌ Обнаружена проблемная структура backend/static/static/"
    echo "🔧 Исправляем структуру..."
    
    # Перемещаем CSS файлы
    if [ -d "backend/static/static/css" ]; then
        echo "📱 Перемещаем CSS файлы..."
        mkdir -p backend/static/css
        mv backend/static/static/css/* backend/static/css/ 2>/dev/null
        rmdir backend/static/static/css 2>/dev/null
    fi
    
    # Перемещаем JS файлы  
    if [ -d "backend/static/static/js" ]; then
        echo "📄 Перемещаем JS файлы..."
        mkdir -p backend/static/js
        mv backend/static/static/js/* backend/static/js/ 2>/dev/null
        rmdir backend/static/static/js 2>/dev/null
    fi
    
    # Удаляем пустую директорию static
    rmdir backend/static/static 2>/dev/null
    
    echo "✅ Структура исправлена!"
else
    echo "✅ Структура файлов корректна"
fi

# Проверяем результат
echo ""
echo "🔍 Финальная проверка:"
./check-static-files.sh 