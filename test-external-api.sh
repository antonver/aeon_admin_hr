#!/bin/bash

echo "🧪 Тестирование внешнего API HR Admin System"
echo "============================================"

# Проверяем, что backend работает
echo "📡 Проверка backend..."
if ! curl -s http://localhost:8001/api/health > /dev/null; then
    echo "❌ Backend не работает"
    echo "Запустите: ./start-backend.sh"
    exit 1
fi

echo "✅ Backend работает"

# Базовый URL
BASE_URL="http://localhost:8001"

echo ""
echo "🔍 Тестирование endpoints..."

# 1. Проверка здоровья API
echo "1. Проверка здоровья API..."
HEALTH_RESPONSE=$(curl -s "$BASE_URL/api/external/health")
echo "Ответ: $HEALTH_RESPONSE"

# 2. Отправка тестовых результатов
echo ""
echo "2. Отправка тестовых результатов..."
TEST_DATA='{
  "full_name": "Тестовый Кандидат",
  "telegram_username": "@test_candidate",
  "telegram_id": "123456789",
  "results": "Кандидат прошел техническое интервью успешно. Опыт работы с Python, FastAPI, React. Рекомендуется к найму."
}'

SUBMIT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/external/submit-results" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

echo "Ответ: $SUBMIT_RESPONSE"

# Извлекаем candidate_id из ответа
CANDIDATE_ID=$(echo "$SUBMIT_RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('candidate_id', 'не найден'))
except:
    print('ошибка парсинга')
")

echo "ID кандидата: $CANDIDATE_ID"

# 3. Получение результатов (если кандидат создан)
if [ "$CANDIDATE_ID" != "не найден" ] && [ "$CANDIDATE_ID" != "ошибка парсинга" ]; then
    echo ""
    echo "3. Получение результатов кандидата..."
    GET_RESPONSE=$(curl -s "$BASE_URL/api/external/results/$CANDIDATE_ID")
    echo "Ответ: $GET_RESPONSE"
fi

echo ""
echo "🎉 Тестирование завершено!"
echo ""
echo "📱 Веб-интерфейс для тестирования:"
echo "   $BASE_URL/test-external-api"
echo ""
echo "📚 Документация API:"
echo "   EXTERNAL_API_GUIDE.md" 