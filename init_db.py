from app import app
from models import db, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create database tables
        db.create_all()

        # Check if admin user exists
        user = db.session.execute(db.select(User).filter_by(username='admin')).scalar_one_or_none()
        if not user:
            print("Creating default admin user...")
            hashed_password = generate_password_hash('password', method='scrypt')
            new_user = User(username='admin', name='Administrator', password=hashed_password) # type: ignore
            db.session.add(new_user)
            db.session.commit()
            print("Admin user created (username: admin, password: password)")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
