"""
WSGI приложение для совместимости с Render
Импортирует FastAPI приложение из backend/main.py
"""

import sys
import os

# Добавляем backend в путь
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Добавляем корень проекта в путь для импорта app.database
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем FastAPI приложение
from main import app

# Создаем WSGI приложение для gunicorn
application = app 