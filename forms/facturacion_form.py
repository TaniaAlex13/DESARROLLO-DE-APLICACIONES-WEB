from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    id_cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    fecha = DateField(
        "Fecha",
        validators=[
            DataRequired()
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                message="El total debe ser mayor o igual a 0."
            )
        ]
    )

    submit = SubmitField(
        "Guardar factura"
    )