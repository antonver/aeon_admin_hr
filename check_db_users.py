#!/usr/bin/env python3
import os
import requests
import json

# URL приложения
BASE_URL = "https://aeon-hr-admin-8568102b383d.herokuapp.com"

def check_users_via_api():
    """Проверяем пользователей через API"""
    print("=== Проверка пользователей через API ===")
    
    # Сначала аутентифицируемся
    auth_response = requests.post(
        f"{BASE_URL}/api/telegram/telegram-auth",
        json={"init_data": "id=123456789&first_name=Test&last_name=User&username=testuser&auth_date=1234567890&hash=test_hash"},
        headers={"Content-Type": "application/json"}
    )
    
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data['access_token']
        user = auth_data['user']
        
        print(f"Аутентифицированный пользователь:")
        print(f"  ID: {user['id']}")
        print(f"  Name: {user['name']}")
        print(f"  Telegram ID: {user['telegram_id']}")
        print(f"  Username: {user['telegram_username']}")
        print(f"  is_admin: {user['is_admin']} (тип: {type(user['is_admin'])})")
        
        # Проверяем профиль
        profile_response = requests.get(
            f"{BASE_URL}/api/telegram/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f"\nДанные профиля:")
            print(f"  is_admin: {profile_data['is_admin']} (тип: {type(profile_data['is_admin'])})")
        
        # Проверяем список админов
        admins_response = requests.get(
            f"{BASE_URL}/api/telegram/admins",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if admins_response.status_code == 200:
            admins_data = admins_response.json()
            print(f"\nСписок администраторов:")
            for admin in admins_data['admins']:
                print(f"  - {admin['name']} (@{admin['telegram_username']}) - is_admin: {admin['is_admin']}")
        else:
            print(f"Ошибка получения списка админов: {admins_response.status_code}")
            print(f"Ответ: {admins_response.text}")
    
    else:
        print(f"Ошибка аутентификации: {auth_response.status_code}")
        print(f"Ответ: {auth_response.text}")

if __name__ == "__main__":
    check_users_via_api() 