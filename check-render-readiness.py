#!/usr/bin/env python3
"""
Скрипт для проверки готовности проекта к деплою на Render
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Проверяет существование файла"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - НЕ НАЙДЕН")
        return False

def check_requirements():
    """Проверяет requirements.txt"""
    if check_file_exists("backend/requirements.txt", "Python requirements"):
        with open("backend/requirements.txt", "r") as f:
            content = f.read()
            if "fastapi" in content and "uvicorn" in content:
                print("✅ Основные зависимости FastAPI найдены")
                return True
            else:
                print("❌ Отсутствуют основные зависимости FastAPI")
                return False
    return False

def check_package_json():
    """Проверяет package.json"""
    if check_file_exists("frontend/package.json", "Node.js package.json"):
        with open("frontend/package.json", "r") as f:
            content = f.read()
            if "react" in content and "build" in content:
                print("✅ React и build script найдены")
                return True
            else:
                print("❌ Отсутствуют React или build script")
                return False
    return False

def check_render_files():
    """Проверяет файлы для Render"""
    files_to_check = [
        ("render.yaml", "Render конфигурация"),
        ("build.sh", "Скрипт сборки"),
        ("start.sh", "Скрипт запуска"),
        ("backend/Dockerfile", "Dockerfile для бэкенда"),
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_scripts_permissions():
    """Проверяет права на выполнение скриптов"""
    scripts = ["build.sh", "start.sh"]
    all_executable = True
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} - исполняемый")
            else:
                print(f"❌ {script} - НЕ исполняемый")
                all_executable = False
        else:
            print(f"❌ {script} - не найден")
            all_executable = False
    
    return all_executable

def check_env_variables():
    """Проверяет переменные окружения"""
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY", 
        "BOT_TOKEN"
    ]
    
    optional_vars = [
        "NOTION_TOKEN",
        "NOTION_DATABASE_ID",
        "TELEGRAM_CHAT_ID"
    ]
    
    print("\n📋 Переменные окружения:")
    print("Обязательные:")
    for var in required_vars:
        print(f"  - {var}")
    
    print("\nОпциональные:")
    for var in optional_vars:
        print(f"  - {var}")
    
    return True

def main():
    """Основная функция проверки"""
    print("🔍 Проверка готовности к деплою на Render")
    print("=" * 50)
    
    checks = [
        ("Файлы проекта", check_render_files),
        ("Python зависимости", check_requirements),
        ("Node.js зависимости", check_package_json),
        ("Права на скрипты", check_scripts_permissions),
        ("Переменные окружения", check_env_variables),
    ]
    
    results = []
    for description, check_func in checks:
        print(f"\n🔍 {description}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Ошибка при проверке: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Результаты проверки:")
    
    if all(results):
        print("✅ Проект готов к деплою на Render!")
        print("\n📝 Следующие шаги:")
        print("1. Запушьте код в Git репозиторий")
        print("2. Создайте аккаунт на Render.com")
        print("3. Создайте новый Blueprint и подключите репозиторий")
        print("4. Настройте переменные окружения")
        print("5. Запустите деплой")
        print("\n📖 Подробные инструкции: RENDER_DEPLOYMENT.md")
    else:
        print("❌ Проект НЕ готов к деплою")
        print("Исправьте найденные проблемы и запустите проверку снова")
        sys.exit(1)

if __name__ == "__main__":
    main() 