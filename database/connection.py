import sqlite3
import os

# Ruta absoluta a la base de datos, junto a este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "stock.db")

def get_connection():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Devuelve filas como diccionarios en vez de tuplas
    conn.row_factory = sqlite3.Row
    return conn