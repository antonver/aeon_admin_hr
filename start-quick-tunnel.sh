#!/bin/bash

echo "🚀 Запуск быстрого Cloudflare туннеля..."

# Проверяем, что backend работает
echo "📡 Проверка backend..."
if ! curl -s http://localhost:8001/api/health > /dev/null; then
    echo "❌ Backend не работает на порту 8001"
    echo "Запустите сначала: ./start-backend.sh"
    exit 1
fi

echo "✅ Backend работает"

# Запускаем туннель с подробным выводом
echo "🌐 Создание Cloudflare туннеля..."
echo "Это может занять 1-2 минуты..."

# Запускаем туннель и сохраняем вывод
cloudflared tunnel --url http://localhost:8001 2>&1 | tee tunnel-output.log &

# Ждем и ищем URL в выводе
echo "⏳ Ожидание создания туннеля..."
for i in {1..30}; do
    if grep -q "https://.*trycloudflare.com" tunnel-output.log; then
        echo ""
        echo "🎉 Туннель создан!"
        echo "📱 Публичная ссылка:"
        grep "https://.*trycloudflare.com" tunnel-output.log | tail -1
        echo ""
        echo "🔗 Приложение доступно по ссылке выше"
        echo "🛑 Для остановки нажмите Ctrl+C"
        break
    fi
    echo -n "."
    sleep 2
done

if ! grep -q "https://.*trycloudflare.com" tunnel-output.log; then
    echo ""
    echo "❌ Не удалось создать туннель за 60 секунд"
    echo "Проверьте логи в файле tunnel-output.log"
    exit 1
fi

# Ждем завершения
wait 