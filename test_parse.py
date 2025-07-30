#!/usr/bin/env python3
import urllib.parse

# Тестовые данные
mock_init_data = "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22en%22%7D&auth_date=1234567890&hash=test_hash"

print("Исходные данные:")
print(mock_init_data)
print()

# Парсим данные
parsed_data = urllib.parse.parse_qs(mock_init_data)
print("Распарсенные данные:")
for key, value in parsed_data.items():
    print(f"{key}: {value}")

print()

# Извлекаем данные пользователя
user_data = {}
for key, value in parsed_data.items():
    if key != 'hash':
        user_data[key] = value[0] if value else None

print("Данные пользователя:")
for key, value in user_data.items():
    print(f"{key}: {value}")

print()

# Проверяем наличие user
if 'user' in user_data:
    print("✅ Поле 'user' найдено")
    print(f"Значение: {user_data['user']}")
else:
    print("❌ Поле 'user' не найдено")
    print(f"Доступные поля: {list(user_data.keys())}") 