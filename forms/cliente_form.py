from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    cedula = StringField(
        "Cédula",
        validators=[
            DataRequired(),
            Length(min=10, max=20)
        ]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(min=7, max=15)
        ]
    )

    submit = SubmitField("Guardar cliente")