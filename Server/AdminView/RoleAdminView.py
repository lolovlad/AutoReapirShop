from flask_admin.contrib.sqla import ModelView


class RoleAdminView(ModelView):
    form_labels = {
        'name': "Название",
        'description': "Описание"
    }

    column_labels = dict(name='Название',
                         description='Описание')
