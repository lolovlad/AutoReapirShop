from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from re import search


class AutoForm(FlaskForm):
    model = StringField("Модель", validators=[DataRequired(), Length(min=2, max=32)])
    brand = StringField("Марка", validators=[DataRequired(), Length(min=2, max=32)])
    number = StringField("Номер", validators=[DataRequired(), Length(min=2, max=6)])

    region = StringField("Регион", validators=[DataRequired(), Length(min=2, max=3)])
    vin_number = StringField("Вин номер", validators=[DataRequired()])
    submit = SubmitField("Сохранить")
