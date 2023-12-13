from flask_admin.contrib.sqla import ModelView
from Server.database import Service
from uuid import uuid4


class ServiceAdminView(ModelView):
    form_columns = [
        'name',
        'price',
        'type',
    ]

    def on_model_change(self, form, model: Service, is_created):
        model.trace_id = str(uuid4())
