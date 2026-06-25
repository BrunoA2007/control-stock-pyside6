from database.connection import get_connection

def inicializar_db():
    """Crea todas las tablas del sistema si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS productos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            precio      REAL    NOT NULL,
            stock       INTEGER NOT NULL DEFAULT 0,
            categoria   TEXT,
            created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            total       REAL    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id     INTEGER NOT NULL,
            producto_id  INTEGER NOT NULL,
            cantidad     INTEGER NOT NULL,
            precio_unit  REAL    NOT NULL,
            FOREIGN KEY (venta_id)    REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")