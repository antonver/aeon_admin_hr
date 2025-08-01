#!/usr/bin/env python3
"""
Скрипт для тестирования системы уведомлений через Telegram бота
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_notifications():
    print("🧪 Тестирование системы уведомлений")
    print("=" * 50)
    
    # 1. Создаем первого админа (симулируем вход через Telegram)
    print("\n1. Создание администратора...")
    
    init_data = "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22Admin%22%2C%22username%22%3A%22testadmin%22%7D&auth_date=1234567890&hash=test_hash"
    
    auth_response = requests.post(f"{BASE_URL}/api/telegram/telegram-auth", json={
        "init_data": init_data
    })
    
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data["access_token"]
        print(f"✅ Администратор создан: {auth_data['user']['name']}")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Ошибка создания администратора: {auth_response.status_code}")
        print(f"   Response: {auth_response.text}")
        return
    
    # 2. Создаем тестового кандидата
    print("\n2. Создание тестового кандидата...")
    
    candidate_data = {
        "full_name": "Иван Петров",
        "telegram_id": "987654321",
        "telegram_username": "ivan_petrov",
        "results": "Тестовые результаты"
    }
    
    candidate_response = requests.post(f"{BASE_URL}/api/candidates", json=candidate_data)
    
    if candidate_response.status_code == 200:
        candidate = candidate_response.json()
        candidate_id = candidate["id"]
        print(f"✅ Кандидат создан: {candidate['full_name']} (ID: {candidate_id})")
    else:
        print(f"❌ Ошибка создания кандидата: {candidate_response.status_code}")
        print(f"   Response: {candidate_response.text}")
        return
    
    # 3. Тестируем уведомления о интервью
    print("\n3. Тестирование уведомлений о интервью...")
    
    # Создаем несколько логов интервью
    interview_questions = [
        {
            "question": "Расскажите о своем опыте работы",
            "answer": "У меня есть 3 года опыта в разработке веб-приложений на Python и JavaScript",
            "score": 8,
            "category": "опыт"
        },
        {
            "question": "Как вы решаете конфликты в команде?",
            "answer": "Я стараюсь выслушать все стороны и найти компромиссное решение",
            "score": 7,
            "category": "soft_skills"
        },
        {
            "question": "Какие у вас планы на развитие?",
            "answer": "Хочу углубить знания в области машинного обучения и стать тимлидом",
            "score": 9,
            "category": "мотивация"
        },
        {
            "question": "Почему хотите работать в нашей компании?",
            "answer": "Мне нравится миссия компании и возможности для роста",
            "score": 8,
            "category": "мотивация"
        },
        {
            "question": "Как вы относитесь к дедлайнам?",
            "answer": "Всегда стараюсь выполнять задачи вовремя и качественно",
            "score": 9,
            "category": "ответственность"
        }
    ]
    
    for i, question_data in enumerate(interview_questions, 1):
        print(f"   Отправка вопроса {i}/5...")
        
        interview_response = requests.post(
            f"{BASE_URL}/api/candidates/{candidate_id}/interview-logs",
            json=question_data
        )
        
        if interview_response.status_code == 200:
            print(f"   ✅ Вопрос {i} отправлен")
        else:
            print(f"   ❌ Ошибка отправки вопроса {i}: {interview_response.status_code}")
            print(f"      Response: {interview_response.text}")
        
        # Небольшая задержка между вопросами
        time.sleep(1)
    
    # 4. Тестируем ручное уведомление
    print("\n4. Тестирование ручного уведомления...")
    
    test_notification_response = requests.post(f"{BASE_URL}/api/candidates/{candidate_id}/test-notification")
    
    if test_notification_response.status_code == 200:
        print("✅ Тестовое уведомление отправлено")
    else:
        print(f"❌ Ошибка тестового уведомления: {test_notification_response.status_code}")
        print(f"   Response: {test_notification_response.text}")
    
    # 5. Проверяем статус кандидата
    print("\n5. Проверка статуса кандидата...")
    
    candidate_status_response = requests.get(f"{BASE_URL}/api/candidates/{candidate_id}")
    
    if candidate_status_response.status_code == 200:
        candidate_status = candidate_status_response.json()
        print(f"✅ Статус кандидата: {candidate_status['status']}")
        print(f"   Последнее действие: {candidate_status['last_action_type']}")
    else:
        print(f"❌ Ошибка получения статуса: {candidate_status_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print("\n📱 Проверьте Telegram бота - должны прийти уведомления:")
    print("   - О каждом вопросе интервью")
    print("   - О завершении интервью")
    print("   - Тестовое уведомление")

if __name__ == "__main__":
    try:
        test_notifications()
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что бэкенд запущен на http://localhost:8001")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}") 