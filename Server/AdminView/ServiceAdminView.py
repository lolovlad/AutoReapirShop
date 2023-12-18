from flask_admin.contrib.sqla import ModelView
from Server.database import Service
from uuid import uuid4


class ServiceAdminView(ModelView):
    form_columns = [
        'name',
        'price',
        'type',
    ]
    form_excluded_columns = ['trace_id']
    form_labels = {
        'name': "Название",
        'price': "Цена",
        'type': "Тип",
    }

    column_labels = dict(name='Название',
                         price='Цена',
                         type="Тип")

    column_exclude_list = ['trace_id']

    def on_model_change(self, form, model: Service, is_created):
        model.trace_id = str(uuid4())
