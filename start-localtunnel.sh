#!/bin/bash

echo "🚀 Запуск внешнего доступа через Localtunnel"
echo "============================================="

# Проверяем, что backend работает
echo "📡 Проверка backend..."
if ! curl -s http://localhost:8001/api/health > /dev/null; then
    echo "❌ Backend не работает на порту 8001"
    echo "Запустите сначала: ./start-backend.sh"
    exit 1
fi

echo "✅ Backend работает"

# Останавливаем существующие процессы
echo "🛑 Остановка существующих процессов..."
pkill -f localtunnel 2>/dev/null
sleep 2

# Запускаем localtunnel
echo "🌐 Запуск Localtunnel..."
echo "Это может занять несколько секунд..."

# Запускаем localtunnel и сохраняем вывод
npx localtunnel --port 8001 2>&1 | tee localtunnel.log &
TUNNEL_PID=$!

# Ждем и ищем URL в выводе
echo "⏳ Ожидание создания туннеля..."
for i in {1..30}; do
    if grep -q "https://.*loca.lt" localtunnel.log; then
        echo ""
        echo "🎉 Туннель создан!"
        echo "📱 Внешний адрес админки:"
        TUNNEL_URL=$(grep "https://.*loca.lt" localtunnel.log | tail -1 | sed 's/.*https/https/')
        echo "   $TUNNEL_URL"
        echo ""
        echo "🔗 Приложение доступно по ссылке выше"
        echo "📊 API endpoints:"
        echo "   $TUNNEL_URL/api/health"
        echo "   $TUNNEL_URL/api/external/health"
        echo "   $TUNNEL_URL/test-external-api"
        echo ""
        echo "🛑 Для остановки нажмите Ctrl+C"
        break
    fi
    echo -n "."
    sleep 2
done

if ! grep -q "https://.*loca.lt" localtunnel.log; then
    echo ""
    echo "❌ Не удалось создать туннель за 60 секунд"
    echo "Проверьте логи в файле localtunnel.log"
    kill $TUNNEL_PID 2>/dev/null
    exit 1
fi

# Ждем завершения
wait $TUNNEL_PID 