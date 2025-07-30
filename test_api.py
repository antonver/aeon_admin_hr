#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API аутентификации
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Тест здоровья API"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ API работает")
        else:
            print("❌ API не отвечает")
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")

def test_telegram_auth_mock():
    """Тест аутентификации с моковыми данными"""
    # Моковые данные Telegram (для тестирования)
    mock_init_data = "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22en%22%7D&auth_date=1234567890&hash=test_hash"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/telegram/telegram-auth",
            json={"init_data": mock_init_data},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Telegram auth test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Аутентификация успешна")
            print(f"Пользователь: {data.get('user', {}).get('name', 'N/A')}")
            print(f"Админ: {data.get('user', {}).get('is_admin', False)}")
            return data.get('access_token')
        else:
            print(f"❌ Ошибка аутентификации: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

def test_profile(token):
    """Тест получения профиля"""
    if not token:
        print("❌ Нет токена для тестирования профиля")
        return
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/telegram/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Profile test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Профиль получен")
            print(f"Имя: {data.get('name', 'N/A')}")
            print(f"Telegram ID: {data.get('telegram_id', 'N/A')}")
            print(f"Админ: {data.get('is_admin', False)}")
        else:
            print(f"❌ Ошибка получения профиля: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка запроса профиля: {e}")

def test_admins(token):
    """Тест получения списка администраторов"""
    if not token:
        print("❌ Нет токена для тестирования администраторов")
        return
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/telegram/admins",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Admins test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Список администраторов получен")
            for admin in data.get('admins', []):
                print(f"  - {admin.get('name', 'N/A')} (@{admin.get('telegram_username', 'N/A')})")
        else:
            print(f"❌ Ошибка получения администраторов: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка запроса администраторов: {e}")

def main():
    print("🧪 Тестирование API аутентификации")
    print("=" * 50)
    
    # Тест здоровья API
    test_health()
    print()
    
    # Тест аутентификации
    token = test_telegram_auth_mock()
    print()
    
    if token:
        # Тест профиля
        test_profile(token)
        print()
        
        # Тест администраторов
        test_admins(token)
        print()
    
    print("🏁 Тестирование завершено")

if __name__ == "__main__":
    main() 