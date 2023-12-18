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
    form_labels = {
        'client': "Клиент",
        'model': "Модель",
        'brand': "Бренд",
        'number': "Номер",
        'region': "Регион",
        'vin_number': "VIN-номер",
    }

    column_labels = dict(client='Клиент',
                         model='Модель',
                         brand="Бренд",
                         number="Номер",
                         region="Регион",
                         vin_number="VIN-номер")

    column_exclude_list = ['trace_id']

    def on_model_change(self, form, model: Service, is_created):
        model.trace_id = str(uuid4())
