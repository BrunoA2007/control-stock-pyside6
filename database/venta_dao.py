from database.connection import get_connection

class VentaDAO:
    def registrar_venta(self, items):
        """
        Registra una venta completa.
        items: lista de dicts con {producto_id, nombre, cantidad, precio_unit}
        Devuelve el id de la venta creada.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Calcular el total
            total = sum(i["cantidad"] * i["precio_unit"] for i in items)

            # Insertar la venta
            cursor.execute(
                "INSERT INTO ventas (total) VALUES (?)",
                (total,)
            )
            venta_id = cursor.lastrowid

            # Insertar cada item del detalle y descontar stock
            for item in items:
                cursor.execute(
                    """INSERT INTO detalle_ventas
                    (venta_id, producto_id, cantidad, precio_unit)
                    VALUES (?, ?, ?, ?)""",
                    (venta_id, item["producto_id"],
                    item["cantidad"], item["precio_unit"])
                )
                cursor.execute(
                    "UPDATE productos SET stock = stock - ? WHERE id = ?",
                    (item["cantidad"], item["producto_id"])
                )

            conn.commit()
            return venta_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def obtener_todas(self):
        "Devuelve todas las ventas de la mas reciente a la mas antigua."
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id,total,created_at
            FROM ventas
            ORDER BY created_at DESC""",
        )
        ventas = cursor.fetchall()
        conn.close()
        return ventas