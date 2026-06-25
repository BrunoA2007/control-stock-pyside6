from database.connection import get_connection

class ProductoDAO:
    """Maneja todas las operaciones de productos en la base de datos."""

    def obtener_todos(self):
        """Devuelve la lista completa de productos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def insertar(self, nombre, precio, stock, categoria=""):
        """Inserta un producto nuevo. Devuelve el id generado."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock, categoria) VALUES (?, ?, ?, ?)",
            (nombre, precio, stock, categoria)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()
        return nuevo_id

    def actualizar_stock(self, producto_id, nuevo_stock):
        """Actualiza el stock de un producto."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET stock = ? WHERE id = ?",
            (nuevo_stock, producto_id)
        )
        conn.commit()
        conn.close()

    def eliminar(self, producto_id):
        """Elimina un producto por su id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
    
    def buscar_por_nombre(self,texto):
        conn = get_connection()
        cursor = conn.cursor()
        texto_busqueda = f"%{texto}%"
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?",(texto_busqueda,))
        productos = cursor.fetchall()
        conn.close()
        return productos