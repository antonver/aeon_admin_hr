#!/usr/bin/env python3
"""
Простой скрипт для показа статистики тестовых данных
"""

import subprocess
import json

def get_candidates():
    """Получает список кандидатов через curl"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:8000/api/candidates/'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return []
    except:
        return []

def show_statistics():
    """Показывает статистику тестовых данных"""
    
    print("📊 Статистика тестовых данных")
    print("=" * 40)
    
    candidates = get_candidates()
    
    if not candidates:
        print("❌ Не удалось получить данные кандидатов")
        return
    
    print(f"✅ Всего кандидатов: {len(candidates)}")
    
    # Статистика по статусам
    statuses = {}
    for candidate in candidates:
        status = candidate['status']
        statuses[status] = statuses.get(status, 0) + 1
    
    print("\n📈 Распределение по статусам:")
    for status, count in statuses.items():
        percentage = (count / len(candidates)) * 100
        print(f"  • {status}: {count} ({percentage:.1f}%)")
    
    # Показываем примеры кандидатов
    print("\n👥 Примеры кандидатов:")
    for i, candidate in enumerate(candidates[:5]):
        print(f"  {i+1}. {candidate['full_name']}")
        print(f"     Telegram: {candidate['telegram_username']}")
        print(f"     Email: {candidate['email']}")
        print(f"     Статус: {candidate['status']}")
        print()
    
    print("🌐 Доступные URL:")
    print("  • Frontend: http://localhost:3000")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • API Base: http://localhost:8000/api/")
    
    print("\n🎉 Тестовые данные готовы к использованию!")

if __name__ == "__main__":
    show_statistics() 