#!/bin/bash

echo "🔍 Проверяем структуру статических файлов..."
echo ""

# Проверяем основные файлы
echo "📁 Структура backend/static/:"
ls -la backend/static/

echo ""
echo "📄 Проверяем index.html:"
if [ -f "backend/static/index.html" ]; then
    echo "✅ index.html найден"
    
    # Извлекаем имена JS и CSS файлов из index.html
    JS_FILE=$(grep -o 'static/js/main\.[^"]*\.js' backend/static/index.html | head -1)
    CSS_FILE=$(grep -o 'static/css/main\.[^"]*\.css' backend/static/index.html | head -1)
    
    echo "📄 JS файл в HTML: $JS_FILE"
    echo "🎨 CSS файл в HTML: $CSS_FILE"
    
    # Проверяем существование файлов
    if [ -f "backend/$JS_FILE" ]; then
        echo "✅ JS файл существует: backend/$JS_FILE"
    else
        echo "❌ JS файл НЕ СУЩЕСТВУЕТ: backend/$JS_FILE"
    fi
    
    if [ -f "backend/$CSS_FILE" ]; then
        echo "✅ CSS файл существует: backend/$CSS_FILE"
    else
        echo "❌ CSS файл НЕ СУЩЕСТВУЕТ: backend/$CSS_FILE"
    fi
else
    echo "❌ index.html не найден"
fi

echo ""
echo "📁 Содержимое backend/static/js/:"
if [ -d "backend/static/js" ]; then
    ls -la backend/static/js/
else
    echo "❌ Директория backend/static/js не существует"
fi

echo ""
echo "📁 Содержимое backend/static/css/:"
if [ -d "backend/static/css" ]; then
    ls -la backend/static/css/
else
    echo "❌ Директория backend/static/css не существует"
fi

echo ""
echo "🚨 Проверяем проблемную структуру backend/static/static/:"
if [ -d "backend/static/static" ]; then
    echo "❌ ПРОБЛЕМА: backend/static/static/ существует!"
    echo "📁 Содержимое:"
    ls -la backend/static/static/
    echo ""
    echo "🔧 Нужно переместить файлы из backend/static/static/ в backend/static/"
else
    echo "✅ Проблемная директория backend/static/static/ отсутствует"
fi 