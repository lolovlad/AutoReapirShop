from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchOrderWorkerForm(FlaskForm):
    state_order = SelectField("Статус заказа", coerce=int)
    submit = SubmitField("Найти")
