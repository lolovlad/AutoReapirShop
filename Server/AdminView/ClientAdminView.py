from flask_admin.contrib.sqla import ModelView
from ..database import User
from wtforms import PasswordField
from uuid import uuid4


class ClientAdminView(ModelView):
    pass
