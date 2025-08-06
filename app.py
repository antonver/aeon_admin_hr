"""
ASGI приложение для совместимости с Render
Импортирует FastAPI приложение из backend/main.py
"""

import sys
import os

# Добавляем backend в путь для импорта
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Импортируем FastAPI приложение из backend/main.py
from main import app

# Экспортируем ASGI приложение
application = app 