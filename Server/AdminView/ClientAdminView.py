from flask_admin.contrib.sqla import ModelView


class ClientAdminView(ModelView):
    form_excluded_columns = ['trace_id']
    form_labels = {
        'name': "Имя",
        'surname': "Фамилия",
        'patronymics': "Отчество",
        'phone': "Номер",
        'email': "Почта",
        'auto': "Авто"
    }

    column_labels = dict(name='Имя',
                         surname='Фамилия',
                         patronymics="Отчество",
                         phone="Номер",
                         email="Почта")


