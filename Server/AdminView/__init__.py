from .UserAdminView import UserAdminView
from .ClientAdminView import ClientAdminView
from .MenuLink import LogoutMenuLink
from .MyAdminIndexView import MyAdminIndexView
from .ServiceAdminView import ServiceAdminView
from .AutoAdminView import AutoAdminView
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ..database import *

admin = Admin(name="Панель Админ", template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(UserAdminView(User, db.session, name="Пользователь"))
admin.add_view(ClientAdminView(Client, db.session, name="Клиенты"))
admin.add_view(ModelView(Role, db.session, name="Роли"))
admin.add_view(ModelView(Type, db.session, name="Тип услуги"))
admin.add_view(ModelView(StateOrder, db.session, name="Состояние заказа"))
admin.add_view(ServiceAdminView(Service, db.session, name="Услуги"))
admin.add_view(AutoAdminView(Auto, db.session, name="Автомобили"))


admin.add_link(LogoutMenuLink(name="Выход", category="", url="/logout"))
