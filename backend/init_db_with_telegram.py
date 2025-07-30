from app.database import engine, Base, User
from sqlalchemy.orm import sessionmaker
import bcrypt

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Создаем тестового админа (если нужно)
try:
    # Проверяем, есть ли уже пользователи
    existing_users = db.query(User).count()
    
    if existing_users == 0:
        # Создаем тестового админа
        admin_user = User(
            name="Тестовый Админ",
            email="admin@example.com",
            password=bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
            telegram_id="123456789",
            telegram_username="test_admin",
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("Создан тестовый админ:")
        print(f"Email: admin@example.com")
        print(f"Пароль: admin123")
        print(f"Telegram ID: 123456789")
        print(f"Telegram Username: test_admin")
    else:
        print(f"В базе данных уже есть {existing_users} пользователей")
        
except Exception as e:
    print(f"Ошибка при создании тестового админа: {e}")
    db.rollback()
finally:
    db.close()

print("База данных инициализирована успешно!") 