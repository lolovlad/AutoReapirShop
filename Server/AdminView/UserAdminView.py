from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
from ..database import User
from wtforms import PasswordField
from uuid import uuid4
from re import search
from flask import flash



class UserAdminView(ModelView):
    excluded_list_columns = ("password_hash", )
    form_extra_fields = {
        'password': PasswordField('Password')
    }
    form_columns = [
        'name',
        'surname',
        'patronymics',
        'phone',
        'email',
        "password",
        "role"
    ]

    def on_model_change(self, form, model: User, is_created):
        if not search(r"((?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,})", form.password.data):
            raise ValidationError("Пароль должен содержать 1 цифру, любой уникальный символ, Буквы латинского алфавита")
        else:
            model.password = form.password.data
            model.trace_id = str(uuid4())