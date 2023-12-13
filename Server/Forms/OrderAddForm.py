from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, TextAreaField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from re import search


class OrderAddForm(FlaskForm):
    auto_mechanic = SelectField("Автомеханник", coerce=int)
    auto = SelectField("Машина", coerce=int)
    state_order = SelectField("Состояние", coerce=int)

    description = TextAreaField("Коментарии")

    services = SelectMultipleField("Услуги", coerce=int)

    submit = SubmitField("Сохранить")