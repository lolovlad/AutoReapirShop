from flask_admin.contrib.sqla import ModelView
from Server.database import Service
from uuid import uuid4


class AutoAdminView(ModelView):
    form_columns = [
        'client',
        'model',
        'brand',
        'number',
        'region',
        'vin_number',
    ]

    def on_model_change(self, form, model: Service, is_created):
        model.trace_id = str(uuid4())
