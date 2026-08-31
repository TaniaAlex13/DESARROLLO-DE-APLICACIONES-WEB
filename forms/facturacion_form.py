from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired()
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired()
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Guardar factura")