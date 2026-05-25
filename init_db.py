import sqlite3

conexion = sqlite3.connect("database.db")

with open("schema.sql") as archivo:

    conexion.executescript(archivo.read())

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")