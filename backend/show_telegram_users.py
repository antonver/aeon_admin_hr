#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import User

def show_telegram_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("Telegram Users:")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Telegram ID: {user.telegram_id}")
            print(f"Telegram Username: {user.telegram_username}")
            print(f"Is Admin: {user.is_admin}")
            print(f"Email: {user.email}")
            print("-" * 80)
    finally:
        db.close()

if __name__ == "__main__":
    show_telegram_users() 