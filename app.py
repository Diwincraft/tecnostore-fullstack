from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# =========================================
# CONFIGURACIÓN
# =========================================

app = Flask(__name__)

# SECRET_KEY con fallback para evitar crash en Render
app.secret_key = os.environ.get("SECRET_KEY", "dev_default_key")

# Carpeta de imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            categoria TEXT,
            imagen TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conexion.commit()
    conexion.close()

init_db()
def seed_admin():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO usuarios (username, password)
            VALUES (?, ?)
        """, (
            "admin",
            generate_password_hash("123456")
        ))

    conexion.commit()
    conexion.close()

seed_admin()

def seed_productos():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        productos_demo = [
            ("Laptop ASUS", 21000, "Laptops", "asus.jpg"),
            ("Mouse Logitech", 450, "Accesorios", "mouse.jpg"),
            ("Teclado Mecánico", 900, "Accesorios", "teclado.jpg"),
            ("Monitor 24\"", 2500, "Pantallas", "monitor.jpg")
        ]

        cursor.executemany("""
            INSERT INTO productos (nombre, precio, categoria, imagen)
            VALUES (?, ?, ?, ?)
        """, productos_demo)

    conexion.commit()
    conexion.close()

seed_productos()
# =========================================
# HOME
# =========================================

@app.route('/')
def inicio():
    conexion = sqlite3.connect("database.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    return render_template("index.html", productos=productos)

# =========================================
# LOGIN
# =========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conexion = sqlite3.connect("database.db")
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE username = ?",
            (username,)
        )

        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario['password'], password):

            session['usuario'] = usuario['username']
            session.permanent = True

            return redirect('/admin')

        else:
            return render_template(
                'login.html',
                error="Usuario o contraseña incorrectos"
            )

    return render_template('login.html')

# =========================================
# LOGOUT
# =========================================

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

# =========================================
# PANEL ADMIN
# =========================================

@app.route('/admin')
def admin():
    if 'usuario' not in session:
        return redirect('/login')

    conexion = sqlite3.connect("database.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    ventas = total_productos * 5

    conexion.close()

    return render_template(
        "admin.html",
        productos=productos,
        total_productos=total_productos,
        total_usuarios=total_usuarios,
        ventas=ventas
    )

# =========================================
# AGREGAR PRODUCTO
# =========================================

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']

        archivo = request.files['imagen']

        nombre_archivo = secure_filename(archivo.filename)

        ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
        archivo.save(ruta)

        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, precio, categoria, imagen)
            VALUES (?, ?, ?, ?)
        """, (nombre, precio, categoria, nombre_archivo))

        conexion.commit()
        conexion.close()

        return redirect('/admin')

    return render_template("agregar_producto.html")

# =========================================
# EDITAR PRODUCTO
# =========================================

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect('/login')

    conexion = sqlite3.connect("database.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']

        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto_actual = cursor.fetchone()

        imagen = producto_actual['imagen']

        archivo = request.files.get('imagen')

        if archivo and archivo.filename != "":
            nombre_archivo = secure_filename(archivo.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
            archivo.save(ruta)
            imagen = nombre_archivo

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, precio = ?, categoria = ?, imagen = ?
            WHERE id = ?
        """, (nombre, precio, categoria, imagen, id))

        conexion.commit()
        conexion.close()

        return redirect('/admin')

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()

    return render_template('editar_producto.html', producto=producto)

# =========================================
# ELIMINAR PRODUCTO
# =========================================

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect('/login')

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

    conexion.commit()
    conexion.close()

    return redirect('/admin')


# =========================================
# EJECUCIÓN LOCAL
# =========================================

if __name__ == '__main__':
    app.run()