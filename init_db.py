from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

def init_database(app, db, Doctor):
    with app.app_context():
        db.create_all()
        if not Doctor.query.first():
            default_doctor = Doctor(username="admin", password=generate_password_hash("admin123"))
            db.session.add(default_doctor)
            db.session.commit()
            print("✅ Default doctor created: admin / admin123")
