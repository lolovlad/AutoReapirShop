from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo


class OrderUpdateForm(FlaskForm):
    state_order = SelectField("Состояние", coerce=int)

    description = TextAreaField("Коментарии")
    services = SelectMultipleField("Услуги", coerce=int)

    submit = SubmitField("Сохранить")