from app import db, Doctor
from werkzeug.security import generate_password_hash

def init_database():
    db.create_all()
    if not Doctor.query.first():
        default = Doctor(username="admin", password=generate_password_hash("admin123"))
        db.session.add(default)
        db.session.commit()
        print("✅ Default doctor created: admin / admin123")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        init_database()