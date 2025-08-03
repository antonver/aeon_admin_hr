"""
ASGI приложение для совместимости с Render
Импортирует FastAPI приложение из main.py
"""

# Импортируем FastAPI приложение
from main import app

# Экспортируем ASGI приложение
application = app 