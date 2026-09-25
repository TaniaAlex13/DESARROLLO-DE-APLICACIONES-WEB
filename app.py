from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import obtener_conexion


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-semana-12"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, usuario FROM usuarios WHERE id = %s",
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(usuario["id"], usuario["usuario"])

    return None

# =========================
# REGISTRO DE USUARIO
# =========================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Verificar si el usuario ya existe
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conexion.close()

            flash("El usuario ya existe.", "danger")

            return render_template(
                "registro.html",
                form=form
            )

        # Encriptar contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        # Registrar usuario
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente.", "success")

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )
# =========================
# INICIO DE SESIÓN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_objeto = Usuario(
                usuario["id"],
                usuario["usuario"]
            )

            login_user(usuario_objeto)

            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template(
        "login.html",
        form=form
    )

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================
# CERRAR SESIÓN
# =========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("login"))

# =========================
# DATOS TEMPORALES
# =========================

clientes_lista = [
    {
        "nombre": "Juan Perez",
        "correo": "juan@gmail.com",
        "telefono": "0991234567",
        "estado": "Activo"
    },
    {
        "nombre": "Maria Lopez",
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
        "contacto": "Pedro Gomez",
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
        "cliente": "Juan Perez",
        "total": 50.00,
        "estado": "Pagada"
    },
    {
        "numero": "001-001-000002",
        "cliente": "Maria Lopez",
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
    nombre_sistema = "Sistema de Gestion Comercial"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# =========================
# PRODUCTOS - MYSQL
# =========================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM productos
        ORDER BY id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


@app.route("/formulario-producto", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return "Producto registrado correctamente"

    if form.is_submitted():

        print("Errores del formulario:")
        print(form.errors)

    return render_template(
        "formulario_producto.html",
        form=form
    )

# =========================
# MODIFICAR PRODUCTO
# =========================

@app.route("/editar-producto/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if producto is None:
        return "Producto no encontrado"

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    return render_template(
        "formulario_producto.html",
        form=form
    )

# =========================
# ELIMINAR PRODUCTO
# =========================

@app.route("/eliminar-producto/<int:id_producto>")
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))

# =========================
# CLIENTES
# =========================

@app.route("/clientes")
@login_required
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


@app.route("/formulario-cliente", methods=["GET", "POST"])
@login_required
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


# =========================
# PROVEEDORES
# =========================

@app.route("/proveedores")
@login_required
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


@app.route("/formulario-proveedor", methods=["GET", "POST"])
@login_required
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


# =========================
# FACTURACIÓN
# =========================

@app.route("/facturacion")
@login_required
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


@app.route("/formulario-facturacion", methods=["GET", "POST"])
@login_required
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


# =========================
# EJECUTAR APLICACIÓN
# =========================

if __name__ == "__main__":
    app.run(debug=True)