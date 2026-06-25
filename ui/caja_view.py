from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QSpinBox, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from database.producto_dao import ProductoDAO
from database.venta_dao import VentaDAO

class CajaView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("CajaView")
        self.dao_producto = ProductoDAO()
        self.dao_venta    = VentaDAO()
        self._carrito     = []  # lista de items en la venta actual
        self._construir_ui()
        self._aplicar_estilos()

    def _construir_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ── Columna izquierda: buscador de productos ──
        col_izq = QVBoxLayout()
        col_izq.setAlignment(Qt.AlignTop)

        titulo_izq = QLabel("Productos")
        titulo_izq.setStyleSheet("font-size: 18px; font-weight: bold;")
        col_izq.addWidget(titulo_izq)

        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar producto...")
        self.campo_busqueda.textChanged.connect(self._filtrar_productos)
        col_izq.addWidget(self.campo_busqueda)

        self.lista_productos = QTableWidget()
        self.lista_productos.setColumnCount(4)
        self.lista_productos.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Precio", "Stock"]
        )
        self.lista_productos.horizontalHeader().setStretchLastSection(True)
        self.lista_productos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lista_productos.setSelectionBehavior(QTableWidget.SelectRows)
        self.lista_productos.setSelectionMode(QTableWidget.SingleSelection)
        self.lista_productos.setColumnHidden(0, True)
        col_izq.addWidget(self.lista_productos)

        # Cantidad y botón agregar
        fila_agregar = QHBoxLayout()
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setMaximum(999)
        self.spin_cantidad.setValue(1)

        btn_agregar = QPushButton("Agregar al carrito")
        btn_agregar.clicked.connect(self._agregar_al_carrito)

        fila_agregar.addWidget(QLabel("Cantidad:"))
        fila_agregar.addWidget(self.spin_cantidad)
        fila_agregar.addWidget(btn_agregar)
        col_izq.addLayout(fila_agregar)

        layout.addLayout(col_izq, stretch=2)

        # ── Columna derecha: carrito y total ──
        col_der = QVBoxLayout()
        col_der.setAlignment(Qt.AlignTop)

        titulo_der = QLabel("Venta actual")
        titulo_der.setStyleSheet("font-size: 18px; font-weight: bold;")
        col_der.addWidget(titulo_der)

        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(4)
        self.tabla_carrito.setHorizontalHeaderLabels(
            ["Producto", "Precio", "Cant.", "Subtotal"]
        )
        self.tabla_carrito.horizontalHeader().setStretchLastSection(True)
        self.tabla_carrito.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_carrito.setSelectionBehavior(QTableWidget.SelectRows)
        col_der.addWidget(self.tabla_carrito)

        # Total
        self.label_total = QLabel("Total: $0.00")
        self.label_total.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 8px 0px;"
        )
        col_der.addWidget(self.label_total)

        # Botones
        btn_quitar = QPushButton("Quitar seleccionado")
        btn_quitar.setObjectName("btn_quitar")
        btn_quitar.clicked.connect(self._quitar_del_carrito)
        col_der.addWidget(btn_quitar)

        btn_confirmar = QPushButton("Confirmar venta")
        btn_confirmar.setObjectName("btn_confirmar")
        btn_confirmar.clicked.connect(self._confirmar_venta)
        col_der.addWidget(btn_confirmar)

        btn_cancelar = QPushButton("Cancelar venta")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.clicked.connect(self._cancelar_venta)
        col_der.addWidget(btn_cancelar)

        layout.addLayout(col_der, stretch=1)

    # ── Métodos de lógica ──────────────────────────

    def showEvent(self, event):
        """Se ejecuta cada vez que el panel se hace visible."""
        super().showEvent(event)
        self._cargar_productos()

    def _cargar_productos(self):
        productos = self.dao_producto.obtener_todos()
        self._poblar_lista(productos)

    def _filtrar_productos(self, texto):
        if texto.strip() == "":
            productos = self.dao_producto.obtener_todos()
        else:
            productos = self.dao_producto.buscar_por_nombre(texto)
        self._poblar_lista(productos)

    def _poblar_lista(self, productos):
        self.lista_productos.setRowCount(0)
        for fila, p in enumerate(productos):
            self.lista_productos.insertRow(fila)
            self.lista_productos.setItem(fila, 0, QTableWidgetItem(str(p["id"])))
            self.lista_productos.setItem(fila, 1, QTableWidgetItem(p["nombre"]))
            self.lista_productos.setItem(fila, 2, QTableWidgetItem(f"${p['precio']:.2f}"))
            self.lista_productos.setItem(fila, 3, QTableWidgetItem(str(p["stock"])))

    def _agregar_al_carrito(self):
        fila = self.lista_productos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Seleccioná un producto primero.")
            return

        producto_id = int(self.lista_productos.item(fila, 0).text())
        nombre      = self.lista_productos.item(fila, 1).text()
        precio_txt  = self.lista_productos.item(fila, 2).text().replace("$", "")
        precio      = float(precio_txt)
        stock       = int(self.lista_productos.item(fila, 3).text())
        cantidad    = self.spin_cantidad.value()

        if cantidad > stock:
            QMessageBox.warning(
                self, "Stock insuficiente",
                f"Solo hay {stock} unidades disponibles de '{nombre}'."
            )
            return

        # Si el producto ya está en el carrito, sumamos la cantidad
        for item in self._carrito:
            if item["producto_id"] == producto_id:
                if item["cantidad"] + cantidad > stock:
                    QMessageBox.warning(
                        self, "Stock insuficiente",
                        f"No podés agregar más de {stock} unidades de '{nombre}'."
                    )
                    return
                item["cantidad"] += cantidad
                self._actualizar_tabla_carrito()
                return

        # Si es nuevo, lo agregamos
        self._carrito.append({
            "producto_id": producto_id,
            "nombre":      nombre,
            "precio_unit": precio,
            "cantidad":    cantidad
        })
        self._actualizar_tabla_carrito()

    def _actualizar_tabla_carrito(self):
        self.tabla_carrito.setRowCount(0)
        total = 0
        for fila, item in enumerate(self._carrito):
            subtotal = item["cantidad"] * item["precio_unit"]
            total += subtotal
            self.tabla_carrito.insertRow(fila)
            self.tabla_carrito.setItem(fila, 0, QTableWidgetItem(item["nombre"]))
            self.tabla_carrito.setItem(fila, 1, QTableWidgetItem(f"${item['precio_unit']:.2f}"))
            self.tabla_carrito.setItem(fila, 2, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_carrito.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))
        self.label_total.setText(f"Total: ${total:.2f}")

    def _quitar_del_carrito(self):
        fila = self.tabla_carrito.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Seleccioná un item del carrito.")
            return
        self._carrito.pop(fila)
        self._actualizar_tabla_carrito()

    def _confirmar_venta(self):
        if not self._carrito:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        total = sum(i["cantidad"] * i["precio_unit"] for i in self._carrito)
        confirmar = QMessageBox.question(
            self, "Confirmar venta",
            f"¿Confirmar venta por ${total:.2f}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            try:
                self.dao_venta.registrar_venta(self._carrito)
                QMessageBox.information(
                    self, "Éxito", "¡Venta registrada correctamente!"
                )
                self._cancelar_venta()
                self._cargar_productos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar: {e}")

    def _cancelar_venta(self):
        self._carrito = []
        self._actualizar_tabla_carrito()
        self.spin_cantidad.setValue(1)

    def _aplicar_estilos(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#CajaView {
                background-color: #f0f2f5;
            }
            QLabel {
                background-color: transparent;
                font-size: 13px;
                color: #2c2f3a;
            }
            QLineEdit, QSpinBox {
                background-color: #ffffff;
                border: 1px solid #c0c4cc;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 13px;
                color: #2c2f3a;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #c0c4cc;
                border-radius: 4px;
                gridline-color: #e4e7ed;
                font-size: 13px;
                color: #2c2f3a;
            }
            QHeaderView::section {
                background-color: #e4e7ed;
                color: #2c2f3a;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4a90d9;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #357abd; }
            QPushButton#btn_confirmar {
                background-color: #27ae60;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton#btn_confirmar:hover { background-color: #219a52; }
            QPushButton#btn_cancelar  { background-color: #e74c3c; }
            QPushButton#btn_cancelar:hover  { background-color: #c0392b; }
        """)