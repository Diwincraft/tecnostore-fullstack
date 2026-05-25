CREATE TABLE productos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    precio REAL NOT NULL,

    categoria TEXT NOT NULL,

    imagen TEXT NOT NULL

);

CREATE TABLE usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL

);