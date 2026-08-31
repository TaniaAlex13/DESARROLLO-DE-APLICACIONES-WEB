from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(min=7, max=15)
        ]
    )

    submit = SubmitField("Guardar proveedor")