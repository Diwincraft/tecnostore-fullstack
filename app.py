from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

import sqlite3
import os

from werkzeug.utils import secure_filename

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# =========================================
# CONFIGURACIÓN
# =========================================

app = Flask(__name__)

app.secret_key = "super_secret_key"

# Carpeta de imágenes

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta si no existe

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================================
# HOME
# =========================================

@app.route('/')
def inicio():

    conexion = sqlite3.connect("database.db")

    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT * FROM productos

    """)

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        "index.html",
        productos=productos
    )

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

        cursor.execute("""

            SELECT * FROM usuarios

            WHERE username = ?

        """, (
            username,
        ))

        usuario = cursor.fetchone()

        conexion.close()

        if usuario and check_password_hash(
            usuario['password'],
            password
        ):

            session['usuario'] = usuario['username']

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

    # PRODUCTOS

    cursor.execute("""

        SELECT * FROM productos

    """)

    productos = cursor.fetchall()

    # TOTAL PRODUCTOS

    cursor.execute("""

        SELECT COUNT(*) FROM productos

    """)

    total_productos = cursor.fetchone()[0]

    # TOTAL USUARIOS

    cursor.execute("""

        SELECT COUNT(*) FROM usuarios

    """)

    total_usuarios = cursor.fetchone()[0]

    # VENTAS SIMULADAS

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

        # IMAGEN

        archivo = request.files['imagen']

        nombre_archivo = secure_filename(
            archivo.filename
        )

        ruta = os.path.join(
            app.config['UPLOAD_FOLDER'],
            nombre_archivo
        )

        archivo.save(ruta)

        imagen = nombre_archivo

        # GUARDAR EN BD

        conexion = sqlite3.connect("database.db")

        cursor = conexion.cursor()

        cursor.execute("""

            INSERT INTO productos
            (
                nombre,
                precio,
                categoria,
                imagen
            )

            VALUES (?, ?, ?, ?)

        """, (
            nombre,
            precio,
            categoria,
            imagen
        ))

        conexion.commit()

        conexion.close()

        return redirect('/admin')

    return render_template(
        "agregar_producto.html"
    )

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

    # =====================================
    # ACTUALIZAR PRODUCTO
    # =====================================

    if request.method == 'POST':

        nombre = request.form['nombre']

        precio = request.form['precio']

        categoria = request.form['categoria']

        # OBTENER PRODUCTO ACTUAL

        cursor.execute(
            "SELECT * FROM productos WHERE id = ?",
            (id,)
        )

        producto_actual = cursor.fetchone()

        imagen = producto_actual['imagen']

        # VERIFICAR NUEVA IMAGEN

        if 'imagen' in request.files:

            archivo = request.files['imagen']

            if archivo.filename != "":

                nombre_archivo = secure_filename(
                    archivo.filename
                )

                ruta = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    nombre_archivo
                )

                archivo.save(ruta)

                imagen = nombre_archivo

        # ACTUALIZAR EN BD

        cursor.execute("""

            UPDATE productos

            SET
                nombre = ?,
                precio = ?,
                categoria = ?,
                imagen = ?

            WHERE id = ?

        """, (
            nombre,
            precio,
            categoria,
            imagen,
            id
        ))

        conexion.commit()

        conexion.close()

        return redirect('/admin')

    # =====================================
    # OBTENER PRODUCTO
    # =====================================

    cursor.execute("""

        SELECT * FROM productos

        WHERE id = ?

    """, (
        id,
    ))

    producto = cursor.fetchone()

    conexion.close()

    return render_template(
        'editar_producto.html',
        producto=producto
    )

# =========================================
# ELIMINAR PRODUCTO
# =========================================

@app.route('/eliminar/<int:id>')
def eliminar(id):

    if 'usuario' not in session:

        return redirect('/login')

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("""

        DELETE FROM productos

        WHERE id = ?

    """, (
        id,
    ))

    conexion.commit()

    conexion.close()

    return redirect('/admin')

# =========================================
# EJECUTAR APP
# =========================================

if __name__ == '__main__':

    app.run(debug=True)