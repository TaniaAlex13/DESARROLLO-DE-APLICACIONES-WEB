from flask import Flask, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion

from forms.proveedor_form import ProveedorForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm


# =========================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-ferreteria"


# =========================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# =========================================================
# MODELO DE USUARIO
# =========================================================

class Usuario(UserMixin):

    def __init__(self, id, usuario, password):

        self.id = id
        self.usuario = usuario
        self.password = password


# =========================================================
# CARGAR USUARIO
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            usuario,
            password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:

        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def inicio():

    return render_template("index.html")


# =========================================================
# REGISTRO
# =========================================================

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
def registro():

    from forms.registro_form import RegistroForm

    form = RegistroForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        password_encriptada = generate_password_hash(
            form.password.data
        )

        try:

            cursor.execute("""
                INSERT INTO usuarios (
                    usuario,
                    password
                )
                VALUES (%s, %s)
            """, (
                form.usuario.data,
                password_encriptada
            ))

            conexion.commit()

        except Exception:

            conexion.rollback()

            cursor.close()
            conexion.close()

            return "El usuario ya existe o ocurrió un error al registrarlo."

        cursor.close()
        conexion.close()

        return redirect(
            url_for("login")
        )

    return render_template(
        "registro.html",
        form=form
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    from forms.login_form import LoginForm

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:

            password_correcta = check_password_hash(
                usuario["password"],
                form.password.data
            )

            if password_correcta:

                usuario_objeto = Usuario(
                    usuario["id"],
                    usuario["usuario"],
                    usuario["password"]
                )

                login_user(usuario_objeto)

                return redirect(
                    url_for("dashboard")
                )

        return render_template(
            "login.html",
            form=form,
            error="Usuario o contraseña incorrectos."
        )

    return render_template(
        "login.html",
        form=form
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# CERRAR SESIÓN
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# =========================================================
# PRODUCTOS - LISTAR
# =========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            productos.id_producto,
            productos.nombre,
            productos.categoria,
            productos.precio,
            productos.stock,
            proveedores.nombre AS proveedor
        FROM productos
        LEFT JOIN proveedores
            ON productos.id_proveedor =
               proveedores.id_proveedor
        ORDER BY productos.id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# =========================================================
# PRODUCTOS - AGREGAR
# =========================================================

@app.route(
    "/formulario-producto",
    methods=["GET", "POST"]
)
@login_required
def formulario_producto():

    form = ProductoForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        cursor.execute("""
            INSERT INTO productos (
                nombre,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("productos")
        )

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================================================
# PRODUCTOS - MODIFICAR
# =========================================================

@app.route(
    "/editar-producto/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    if not producto:

        cursor.close()
        conexion.close()

        return "Producto no encontrado"

    form = ProductoForm()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("productos")
        )

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = float(producto["precio"])
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================================================
# PRODUCTOS - ELIMINAR
# =========================================================

@app.route(
    "/eliminar-producto/<int:id_producto>"
)
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            DELETE FROM productos
            WHERE id_producto = %s
        """, (id_producto,))

        conexion.commit()

    except Exception:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return "No se puede eliminar este producto."

    cursor.close()
    conexion.close()

    return redirect(
        url_for("productos")
    )


# =========================================================
# PROVEEDORES - LISTAR
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# =========================================================
# PROVEEDORES - AGREGAR
# =========================================================

@app.route(
    "/formulario-proveedor",
    methods=["GET", "POST"]
)
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================================================
# PROVEEDORES - MODIFICAR
# =========================================================

@app.route(
    "/editar-proveedor/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    if not proveedor:

        cursor.close()
        conexion.close()

        return "Proveedor no encontrado"

    form = ProveedorForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE proveedores
            SET
                nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id_proveedor
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("proveedores")
        )

    if not form.is_submitted():

        form.nombre.data = proveedor["nombre"]
        form.telefono.data = proveedor["telefono"]
        form.correo.data = proveedor["correo"]

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================================================
# PROVEEDORES - ELIMINAR
# =========================================================

@app.route(
    "/eliminar-proveedor/<int:id_proveedor>"
)
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            DELETE FROM proveedores
            WHERE id_proveedor = %s
        """, (id_proveedor,))

        conexion.commit()

    except Exception:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return (
            "No se puede eliminar este proveedor "
            "porque está relacionado con uno o más "
            "productos. Primero debe modificar o "
            "eliminar los productos que utilizan "
            "este proveedor."
        )

    cursor.close()
    conexion.close()

    return redirect(
        url_for("proveedores")
    )


# =========================================================
# CLIENTES - LISTAR
# =========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# =========================================================
# CLIENTES - AGREGAR
# =========================================================

@app.route(
    "/formulario-cliente",
    methods=["GET", "POST"]
)
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO clientes (
                nombre,
                cedula,
                telefono,
                correo
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================================================
# CLIENTES - MODIFICAR
# =========================================================

@app.route(
    "/editar-cliente/<int:id_cliente>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    if not cliente:

        cursor.close()
        conexion.close()

        return "Cliente no encontrado"

    form = ClienteForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE clientes
            SET
                nombre = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data,
            id_cliente
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("clientes")
        )

    if not form.is_submitted():

        form.nombre.data = cliente["nombre"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.correo.data = cliente["correo"]

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================================================
# CLIENTES - ELIMINAR
# =========================================================

@app.route(
    "/eliminar-cliente/<int:id_cliente>"
)
@login_required
def eliminar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            DELETE FROM clientes
            WHERE id_cliente = %s
        """, (id_cliente,))

        conexion.commit()

    except Exception:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return (
            "No se puede eliminar este cliente "
            "porque está relacionado con una o más "
            "facturas."
        )

    cursor.close()
    conexion.close()

    return redirect(
        url_for("clientes")
    )


# =========================================================
# FACTURACIÓN - LISTAR
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            facturas.id_factura,
            clientes.nombre AS cliente,
            facturas.fecha,
            facturas.total
        FROM facturas
        INNER JOIN clientes
            ON facturas.id_cliente = clientes.id_cliente
        ORDER BY facturas.id_factura
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# =========================================================
# FACTURACIÓN - AGREGAR
# =========================================================

@app.route(
    "/formulario-facturacion",
    methods=["GET", "POST"]
)
@login_required
def formulario_facturacion():

    form = FacturacionForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    form.id_cliente.choices = [
        (
            cliente["id_cliente"],
            cliente["nombre"]
        )
        for cliente in clientes
    ]

    if form.validate_on_submit():

        cursor.execute("""
            INSERT INTO facturas (
                id_cliente,
                fecha,
                total
            )
            VALUES (%s, %s, %s)
        """, (
            form.id_cliente.data,
            form.fecha.data,
            form.total.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("facturacion")
        )

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# =========================================================
# FACTURACIÓN - MODIFICAR
# =========================================================

@app.route(
    "/editar-factura/<int:id_factura>",
    methods=["GET", "POST"]
)
@login_required
def editar_factura(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_factura,
            id_cliente,
            fecha,
            total
        FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    if not factura:

        cursor.close()
        conexion.close()

        return "Factura no encontrada"

    form = FacturacionForm()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    form.id_cliente.choices = [
        (
            cliente["id_cliente"],
            cliente["nombre"]
        )
        for cliente in clientes
    ]

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE facturas
            SET
                id_cliente = %s,
                fecha = %s,
                total = %s
            WHERE id_factura = %s
        """, (
            form.id_cliente.data,
            form.fecha.data,
            form.total.data,
            id_factura
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(
            url_for("facturacion")
        )

    if not form.is_submitted():

        form.id_cliente.data = factura["id_cliente"]
        form.fecha.data = factura["fecha"]
        form.total.data = float(factura["total"])

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# =========================================================
# FACTURACIÓN - ELIMINAR
# =========================================================

@app.route(
    "/eliminar-factura/<int:id_factura>"
)
@login_required
def eliminar_factura(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            DELETE FROM facturas
            WHERE id_factura = %s
        """, (id_factura,))

        conexion.commit()

    except Exception:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return "No se puede eliminar esta factura."

    cursor.close()
    conexion.close()

    return redirect(
        url_for("facturacion")
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )