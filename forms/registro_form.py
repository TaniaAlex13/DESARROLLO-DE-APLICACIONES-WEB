from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistroForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=4, max=255)
        ]
    )

    submit = SubmitField("Registrarse")