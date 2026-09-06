from flask import Flask, render_template
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

import sqlite3
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-semana-11"

# =========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =========================================================

DATABASE = "data/ferreteria.db"


def conectar_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def crear_base_datos():
    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)

    conn = conectar_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Crear la base de datos y la tabla al iniciar la aplicación
crear_base_datos()


# =========================================================
# DATOS DE CLIENTES, PROVEEDORES Y FACTURACIÓN
# =========================================================

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


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def inicio():
    nombre_sistema = "Sistema de Gestión Comercial"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# =========================================================
# PRODUCTOS - SELECT DESDE SQLITE
# =========================================================

@app.route("/productos")
def productos():

    conn = conectar_db()

    cursor = conn.execute("""
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id
    """)

    productos = cursor.fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# =========================================================
# FORMULARIO DE PRODUCTOS - INSERT EN SQLITE
# =========================================================

@app.route("/formulario-producto", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_db()

        conn.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        conn.commit()
        conn.close()

        return "Producto registrado correctamente"

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================================================
# CLIENTES
# =========================================================

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
            "telefono": form.telefono.data
        }

        clientes_lista.append(cliente)

        return "Cliente registrado correctamente"

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================================================
# PROVEEDORES
# =========================================================

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

        return "Proveedor registrado correctamente"

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================================================
# FACTURACIÓN
# =========================================================

@app.route("/facturacion")
def facturacion():
    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


@app.route("/formulario-facturacion", methods=["GET", "POST"])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data,
            "estado": form.estado.data
        }

        facturas_lista.append(factura)

        return "Factura registrada correctamente"

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)