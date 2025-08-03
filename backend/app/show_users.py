from backend.app.database import SessionLocal, User

def show_users():
    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        print(f"id={user.id} | name={user.name} | email={user.email} | password={user.password}")
    db.close()

if __name__ == "__main__":
    show_users() 