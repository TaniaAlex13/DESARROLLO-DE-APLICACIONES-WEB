from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm


app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================

app.config["SECRET_KEY"] = "clave-secreta-proyecto"


# =========================
# DATOS DE PRODUCTOS
# =========================

productos_lista = [
    {
        "nombre": "Laptop Lenovo",
        "categoria": "Computación",
        "precio": 650.00,
        "stock": 5
    },
    {
        "nombre": "Mouse inalámbrico",
        "categoria": "Accesorios",
        "precio": 15.00,
        "stock": 10
    },
    {
        "nombre": "Teclado mecánico",
        "categoria": "Accesorios",
        "precio": 45.00,
        "stock": 0
    },
    {
        "nombre": "Monitor LG 24 pulgadas",
        "categoria": "Monitores",
        "precio": 180.00,
        "stock": 3
    }
]


# =========================
# DATOS DE CLIENTES
# =========================

clientes_lista = [
    {
        "nombre": "Juan Pérez",
        "correo": "juan@gmail.com",
        "telefono": "0991234567",
        "estado": "Activo"
    },
    {
        "nombre": "María López",
        "correo": "maria@gmail.com",
        "telefono": "0987654321",
        "estado": "Activo"
    },
    {
        "nombre": "Carlos Andrade",
        "correo": "carlos@gmail.com",
        "telefono": "0974561234",
        "estado": "Inactivo"
    }
]


# =========================
# DATOS DE PROVEEDORES
# =========================

proveedores_lista = [
    {
        "empresa": "Tech Solutions",
        "contacto": "Pedro Gómez",
        "telefono": "0991112233"
    },
    {
        "empresa": "Computec",
        "contacto": "Ana Torres",
        "telefono": "0982223344"
    }
]


# =========================
# DATOS DE FACTURACIÓN
# =========================

facturas_lista = [
    {
        "numero": "001-001-000001",
        "cliente": "Juan Pérez",
        "total": 50.00,
        "estado": "Pagada"
    },
    {
        "numero": "001-001-000002",
        "cliente": "María López",
        "total": 85.00,
        "estado": "Pendiente"
    },
    {
        "numero": "001-001-000003",
        "cliente": "Carlos Andrade",
        "total": 120.00,
        "estado": "Pagada"
    }
]


# =========================
# INICIO
# =========================

@app.route("/")
def inicio():

    nombre_sistema = "Sistema de Gestión Comercial"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# =========================
# PRODUCTOS
# =========================

@app.route("/productos")
def productos():

    return render_template(
        "productos.html",
        productos=productos_lista
    )


@app.route("/formulario-producto", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        productos_lista.append(producto)

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================
# CLIENTES
# =========================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


@app.route("/formulario-cliente", methods=["GET", "POST"])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "estado": "Activo"
        }

        clientes_lista.append(cliente)

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================
# PROVEEDORES
# =========================

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


@app.route("/formulario-proveedor", methods=["GET", "POST"])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data
        }

        proveedores_lista.append(proveedor)

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================
# FACTURACIÓN
# =========================

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


# =========================
# EJECUTAR APLICACIÓN
# =========================

if __name__ == "__main__":
    app.run(debug=True)