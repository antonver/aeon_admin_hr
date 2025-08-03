"""
WSGI приложение для совместимости с Render
Импортирует FastAPI приложение из main.py
"""

# Импортируем FastAPI приложение
from main import app

# Создаем WSGI приложение для gunicorn
application = app 