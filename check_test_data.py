#!/usr/bin/env python3
"""
Скрипт для проверки тестовых данных через API
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def check_api():
    """Проверяет API и показывает тестовые данные"""
    
    print("🔍 Проверка тестовых данных...")
    print("=" * 50)
    
    try:
        # Проверяем кандидатов
        print("📋 Список кандидатов:")
        response = requests.get(f"{BASE_URL}/candidates/")
        if response.status_code == 200:
            candidates = response.json()
            print(f"✅ Найдено {len(candidates)} кандидатов")
            
            # Показываем статистику по статусам
            statuses = {}
            for candidate in candidates:
                status = candidate['status']
                statuses[status] = statuses.get(status, 0) + 1
            
            print("\n📊 Статистика по статусам:")
            for status, count in statuses.items():
                print(f"  • {status}: {count} кандидатов")
            
            # Показываем первых 3 кандидатов
            print("\n👥 Первые 3 кандидата:")
            for i, candidate in enumerate(candidates[:3]):
                print(f"  {i+1}. {candidate['full_name']} (@{candidate['telegram_username']}) - {candidate['status']}")
        
        # Проверяем интервью логи для первого кандидата
        if candidates:
            first_candidate_id = candidates[0]['id']
            print(f"\n📝 Интервью логи для кандидата ID {first_candidate_id}:")
            response = requests.get(f"{BASE_URL}/candidates/{first_candidate_id}/interview-logs/")
            if response.status_code == 200:
                logs = response.json()
                print(f"✅ Найдено {len(logs)} записей интервью")
                for log in logs[:2]:  # Показываем первые 2 записи
                    print(f"  • Вопрос: {log['question']}")
                    print(f"    Ответ: {log['answer'][:50]}...")
                    print(f"    Оценка: {log['score']}/10")
            else:
                print("❌ Не удалось получить логи интервью")
        
        # Проверяем комментарии
        print(f"\n💬 Комментарии HR для кандидата ID {first_candidate_id}:")
        response = requests.get(f"{BASE_URL}/candidates/{first_candidate_id}/comments/")
        if response.status_code == 200:
            comments = response.json()
            print(f"✅ Найдено {len(comments)} комментариев")
            for comment in comments:
                print(f"  • {comment['hr_comment']}")
        else:
            print("❌ Не удалось получить комментарии")
        
        # Проверяем метрики
        print("\n📈 Метрики:")
        response = requests.get(f"{BASE_URL}/metrics/")
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ Общее количество кандидатов: {metrics.get('total_candidates', 'N/A')}")
            print(f"✅ Активных кандидатов: {metrics.get('active_candidates', 'N/A')}")
            print(f"✅ Процент прохождения тестов: {metrics.get('test_pass_rate', 'N/A')}%")
        else:
            print("❌ Не удалось получить метрики")
        
        print("\n" + "=" * 50)
        print("🎉 Проверка завершена! Все тестовые данные доступны.")
        print("\n🌐 Доступные URL:")
        print(f"  • Frontend: http://localhost:3000")
        print(f"  • API Docs: http://localhost:8000/docs")
        print(f"  • API Base: http://localhost:8000/api/")
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к API. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")

if __name__ == "__main__":
    check_api() 