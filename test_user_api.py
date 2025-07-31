#!/usr/bin/env python3
import requests
import json

# URL приложения
BASE_URL = "https://aeon-hr-admin-8568102b383d.herokuapp.com"

def test_telegram_auth():
    """Тестируем аутентификацию через Telegram"""
    print("=== Тестирование Telegram аутентификации ===")
    
    # Симулируем init_data от Telegram
    # В реальном приложении это должно приходить от Telegram
    test_init_data = "id=123456789&first_name=Test&last_name=User&username=testuser&auth_date=1234567890&hash=test_hash"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/telegram/telegram-auth",
            json={"init_data": test_init_data},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"User is_admin: {data['user']['is_admin']}")
            print(f"User is_admin type: {type(data['user']['is_admin'])}")
            return data
        else:
            print("Ошибка аутентификации")
            return None
            
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

def test_profile_endpoint(token):
    """Тестируем endpoint профиля"""
    print("\n=== Тестирование профиля ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/telegram/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"User is_admin: {data['is_admin']}")
            print(f"User is_admin type: {type(data['is_admin'])}")
            return data
        else:
            print("Ошибка получения профиля")
            return None
            
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

if __name__ == "__main__":
    # Тестируем аутентификацию
    auth_data = test_telegram_auth()
    
    if auth_data:
        token = auth_data['access_token']
        # Тестируем профиль
        test_profile_endpoint(token) 