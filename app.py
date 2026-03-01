from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from models import db, User
from views.auth import auth_bp
from views.main import main_bp
from views.admin import MyModelView, MyAdminIndexView
from datetime import datetime
from zoneinfo import ZoneInfo
import dateutil.parser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Initialize Extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

# Filters
@app.template_filter('datetimeformat')
def datetimeformat_filter(value):
    if not value:
        return ""
    try:
        # Betfair returns ISO 8601 strings (e.g., 2026-03-01T14:30:00.000Z)
        dt = dateutil.parser.parse(value)
        
        # Convert to Helsinki time
        # Ensure the parsed datetime is timezone-aware (it usually is if 'Z' is present)
        # If not, assume UTC first
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            
        local_dt = dt.astimezone(ZoneInfo("Europe/Helsinki"))
        
        # Format to Finnish style: dd.mm.yyyy HH:MM
        return local_dt.strftime('%d.%m.%Y %H:%M')
    except Exception as e:
        print(f"Error formatting date: {e}")
        return value

# Admin
admin = Admin(app, name='Betfair Admin', index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
