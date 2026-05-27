import sqlite3

from werkzeug.security import generate_password_hash

conexion = sqlite3.connect("database.db")

cursor = conexion.cursor()

# ELIMINAR ADMIN EXISTENTE

cursor.execute("""

    DELETE FROM usuarios
    WHERE username = ?

""", ("admin",))

# CREAR NUEVO HASH

password_hash = generate_password_hash("123456")

# INSERTAR ADMIN NUEVO

cursor.execute("""

    INSERT INTO usuarios
    (username, password)

    VALUES (?, ?)

""", (
    "admin",
    password_hash
))

conexion.commit()

conexion.close()

print("Administrador creado correctamente")