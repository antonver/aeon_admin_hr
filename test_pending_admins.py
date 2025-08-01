#!/usr/bin/env python3
"""
Скрипт для тестирования функциональности ожидающих админов
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_pending_admins():
    print("🧪 Тестирование функциональности ожидающих админов")
    print("=" * 50)
    
    # 1. Создаем первого админа (симулируем вход через Telegram)
    print("\n1. Создание первого администратора...")
    
    # Симулируем Telegram init_data
    init_data = "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22Admin%22%2C%22username%22%3A%22testadmin%22%7D&auth_date=1234567890&hash=test_hash"
    
    auth_response = requests.post(f"{BASE_URL}/api/telegram/telegram-auth", json={
        "init_data": init_data
    })
    
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data["access_token"]
        print(f"✅ Первый администратор создан: {auth_data['user']['name']}")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Ошибка создания первого админа: {auth_response.status_code}")
        print(f"   Response: {auth_response.text}")
        return
    
    # 2. Добавляем ожидающего админа (используем другой username)
    print("\n2. Добавление ожидающего администратора...")
    
    pending_response = requests.post(f"{BASE_URL}/api/telegram/create-admin", 
        json={"telegram_username": "futureadmin"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if pending_response.status_code == 200:
        pending_data = pending_response.json()
        print(f"✅ Ожидающий администратор добавлен: {pending_data['message']}")
    else:
        print(f"❌ Ошибка добавления ожидающего админа: {pending_response.status_code}")
        print(f"   Response: {pending_response.text}")
        return
    
    # 3. Проверяем список ожидающих админов
    print("\n3. Проверка списка ожидающих администраторов...")
    
    pending_list_response = requests.get(f"{BASE_URL}/api/telegram/pending-admins",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if pending_list_response.status_code == 200:
        pending_list = pending_list_response.json()
        print(f"✅ Список ожидающих администраторов получен:")
        for pending in pending_list["pending_admins"]:
            print(f"   - @{pending['telegram_username']} (добавлен: {pending['created_at']})")
    else:
        print(f"❌ Ошибка получения списка ожидающих: {pending_list_response.status_code}")
        print(f"   Response: {pending_list_response.text}")
    
    # 4. Симулируем вход ожидающего админа
    print("\n4. Симуляция входа ожидающего администратора...")
    
    # Симулируем Telegram init_data для ожидающего админа
    new_init_data = "user=%7B%22id%22%3A987654321%2C%22first_name%22%3A%22Future%22%2C%22last_name%22%3A%22Admin%22%2C%22username%22%3A%22futureadmin%22%7D&auth_date=1234567890&hash=test_hash"
    
    new_auth_response = requests.post(f"{BASE_URL}/api/telegram/telegram-auth", json={
        "init_data": new_init_data
    })
    
    if new_auth_response.status_code == 200:
        new_auth_data = new_auth_response.json()
        print(f"✅ Ожидающий администратор успешно вошел: {new_auth_data['user']['name']}")
        print(f"   Статус админа: {new_auth_data['user']['is_admin']}")
    else:
        print(f"❌ Ошибка входа ожидающего админа: {new_auth_response.status_code}")
        print(f"   Response: {new_auth_response.text}")
    
    # 5. Проверяем, что ожидающий админ исчез из списка
    print("\n5. Проверка, что ожидающий администратор исчез из списка...")
    
    time.sleep(1)  # Небольшая задержка
    
    final_pending_response = requests.get(f"{BASE_URL}/api/telegram/pending-admins",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if final_pending_response.status_code == 200:
        final_pending_list = final_pending_response.json()
        if len(final_pending_list["pending_admins"]) == 0:
            print("✅ Ожидающий администратор успешно удален из списка ожидающих")
        else:
            print(f"❌ Ожидающий администратор все еще в списке: {final_pending_list}")
    else:
        print(f"❌ Ошибка проверки финального списка: {final_pending_response.status_code}")
    
    # 6. Проверяем список всех админов
    print("\n6. Проверка списка всех администраторов...")
    
    admins_response = requests.get(f"{BASE_URL}/api/telegram/admins",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if admins_response.status_code == 200:
        admins_list = admins_response.json()
        print(f"✅ Список всех администраторов:")
        for admin in admins_list["admins"]:
            print(f"   - {admin['name']} (@{admin['telegram_username']}) - {'Админ' if admin['is_admin'] else 'Пользователь'}")
    else:
        print(f"❌ Ошибка получения списка админов: {admins_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")

if __name__ == "__main__":
    try:
        test_pending_admins()
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что бэкенд запущен на http://localhost:8001")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}") 