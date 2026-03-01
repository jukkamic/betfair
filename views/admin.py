from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    def on_model_change(self, form, model, is_created):
        # Hash the password when creating or updating a user via admin
        if form.password.data:
             model.password = generate_password_hash(form.password.data, method='scrypt')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
