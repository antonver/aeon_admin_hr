"""
WSGI приложение для совместимости с Render
Импортирует FastAPI приложение из backend/main.py
"""

import sys
import os

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Импортируем FastAPI приложение
from main import app

# Создаем WSGI приложение для gunicorn
application = app 