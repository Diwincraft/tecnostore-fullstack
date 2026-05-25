import sqlite3

from werkzeug.security import (
    generate_password_hash
)

conexion = sqlite3.connect("database.db")

cursor = conexion.cursor()

password_segura = generate_password_hash("123456")

cursor.execute("""

    INSERT INTO usuarios
    (username, password)

    VALUES (?, ?)

""", (
    "admin",
    password_segura
))

conexion.commit()
conexion.close()

print("Administrador creado correctamente")