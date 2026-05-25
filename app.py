from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

import sqlite3

import sqlite3

import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super_secret_key"

# HOME

@app.route('/')
def inicio():

    conexion = sqlite3.connect("database.db")

    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        "index.html",
        productos=productos
    )

# PANEL ADMIN

@app.route('/admin')
def admin():

    if 'usuario' not in session:

        return redirect('/login')

    conexion = sqlite3.connect("database.db")

    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    # PRODUCTOS

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    # TOTAL PRODUCTOS

    cursor.execute(
        "SELECT COUNT(*) FROM productos"
    )

    total_productos = cursor.fetchone()[0]

    # TOTAL USUARIOS

    cursor.execute(
        "SELECT COUNT(*) FROM usuarios"
    )

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

# LOGIN

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

            return "Credenciales incorrectas"

    return render_template('login.html')

# LOGOUT

@app.route('/logout')
def logout():

    session.pop('usuario', None)

    return redirect('/login')

# AGREGAR PRODUCTO

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        imagen = request.form['imagen']

        conexion = sqlite3.connect("database.db")

        cursor = conexion.cursor()

        cursor.execute("""

            INSERT INTO productos
            (nombre, precio, categoria, imagen)

            VALUES (?, ?, ?, ?)

        """, (nombre, precio, categoria, imagen))

        conexion.commit()
        conexion.close()

        return redirect('/admin')

    return render_template("agregar_producto.html")

# EDITAR PRODUCTO

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    conexion = sqlite3.connect("database.db")

    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    # POST -> guardar cambios

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
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

    # GET -> cargar datos

    cursor.execute(
        "SELECT * FROM productos WHERE id = ?",
        (id,)
    )

    producto = cursor.fetchone()

    conexion.close()

    return render_template(
        'editar_producto.html',
        producto=producto
    )

# ELIMINAR PRODUCTO

@app.route('/eliminar/<int:id>')
def eliminar(id):

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect('/admin')

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

if __name__ == '__main__':

    app.run(debug=True)