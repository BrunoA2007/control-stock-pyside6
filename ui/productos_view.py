from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QLineEdit,
    QPushButton, QLabel, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from database.producto_dao import ProductoDAO

class ProductosView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ProductosView")
        self.setAutoFillBackground(True)
        self.dao = ProductoDAO()
        self._construir_ui()
        self.cargar_tabla()

    def _construir_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(16)

        # ── Lado izquierdo: tabla ──────────────────────────
        lado_izq = QVBoxLayout()

        titulo = QLabel("Productos")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        lado_izq.addWidget(titulo)

        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar por nombre...")
        self.campo_busqueda.textChanged.connect(self.filtrar_tabla)
        lado_izq.addWidget(self.campo_busqueda)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Precio", "Stock", "Categoría"]
        )
        # La última columna ocupa el espacio restante
        self.tabla.horizontalHeader().setStretchLastSection(True)
        # No se puede editar directamente en la tabla
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # Solo se puede seleccionar una fila entera
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        # Ocultar columna ID (la usamos internamente pero no la mostramos)
        self.tabla.setColumnHidden(0, True)
        # Al seleccionar una fila, cargar datos en el formulario
        self.tabla.itemSelectionChanged.connect(self._cargar_en_formulario)

        lado_izq.addWidget(self.tabla)
        layout_principal.addLayout(lado_izq, stretch=2)

        # ── Lado derecho: formulario ───────────────────────
        lado_der = QVBoxLayout()
        lado_der.setAlignment(Qt.AlignTop)

        titulo_form = QLabel("Detalle")
        titulo_form.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        lado_der.addWidget(titulo_form)

        formulario = QFormLayout()
        formulario.setSpacing(10)

        self.campo_nombre    = QLineEdit()
        self.campo_precio    = QLineEdit()
        self.campo_stock     = QLineEdit()
        self.campo_categoria = QLineEdit()

        

        formulario.addRow("Nombre:",    self.campo_nombre)
        formulario.addRow("Precio:",    self.campo_precio)
        formulario.addRow("Stock:",     self.campo_stock)
        formulario.addRow("Categoría:", self.campo_categoria)
        lado_der.addLayout(formulario)
        lado_der.addSpacing(16)

        # Botones
        self.btn_guardar = QPushButton("Guardar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("btn_eliminar")

        self.btn_guardar.clicked.connect(self._guardar_producto)
        self.btn_limpiar.clicked.connect(self._limpiar_formulario)
        self.btn_eliminar.clicked.connect(self._eliminar_producto)

        lado_der.addWidget(self.btn_guardar)
        lado_der.addWidget(self.btn_limpiar)
        lado_der.addWidget(self.btn_eliminar)

        layout_principal.addLayout(lado_der, stretch=1)
        self._aplicar_estilos()

    def _aplicar_estilos(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        QWidget#ProductosView {
        background-color: #f0f2f5;
        }

        QLabel {
        background-color: transparent;
        font-size: 13px;
        color: #2c2f3a;
        }

        QLineEdit {
        background-color: #ffffff;
        border: 1px solid #c0c4cc;
        border-radius: 4px;
        padding: 6px 8px;
        font-size: 13px;
        color: #2c2f3a;
        }

        QLineEdit:focus {
        border: 1px solid #4a90d9;
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

        QPushButton:hover {
        background-color: #357abd;
        }

        QPushButton#btn_eliminar {
        background-color: #e74c3c;
        }

        QPushButton#btn_eliminar:hover {
        background-color: #c0392b;
        }
        """)

    # ── Métodos de lógica ──────────────────────────────────

    def cargar_tabla(self):
        """Carga todos los productos desde la base de datos."""
        productos = self.dao.obtener_todos()
        self._poblar_tabla(productos)

    def filtrar_tabla(self, texto):
        """Filtra la tabla según el texto de búsqueda."""
        if texto.strip() == "":
            productos = self.dao.obtener_todos()
        else:
            productos = self.dao.buscar_por_nombre(texto)
        self._poblar_tabla(productos)

    def _poblar_tabla(self, productos):
        """Llena la tabla con una lista de productos."""
        self.tabla.setRowCount(0)  # limpiar filas anteriores
        for fila, p in enumerate(productos):
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(p["id"])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(p["nombre"]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(p["precio"])))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(p["stock"])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(p["categoria"] or ""))

    def _cargar_en_formulario(self):
        """Cuando se selecciona una fila, carga sus datos en el formulario."""
        filas = self.tabla.selectedItems()
        if not filas:
            return
        fila = self.tabla.currentRow()
        self.campo_nombre.setText(self.tabla.item(fila, 1).text())
        self.campo_precio.setText(self.tabla.item(fila, 2).text())
        self.campo_stock.setText(self.tabla.item(fila, 3).text())
        self.campo_categoria.setText(self.tabla.item(fila, 4).text())

    def _guardar_producto(self):
        """Inserta un producto nuevo o actualiza el seleccionado."""
        nombre    = self.campo_nombre.text().strip()
        precio    = self.campo_precio.text().strip()
        stock     = self.campo_stock.text().strip()
        categoria = self.campo_categoria.text().strip()

        # Validaciones básicas
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
            return
        try:
            precio = float(precio)
            stock  = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio y stock deben ser números.")
            return

        self.dao.insertar(nombre, precio, stock, categoria)
        QMessageBox.information(self, "Éxito", "Producto guardado correctamente.")
        self._limpiar_formulario()
        self.cargar_tabla()

    def _limpiar_formulario(self):
        """Vacía todos los campos del formulario."""
        for campo in [self.campo_nombre, self.campo_precio,self.campo_stock, self.campo_categoria]:
            campo.clear()
        self.tabla.clearSelection()

    def _eliminar_producto(self):
        """Elimina el producto seleccionado en la tabla."""
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Seleccioná un producto primero.")
            return

        nombre = self.tabla.item(fila, 1).text()
        confirmar = QMessageBox.question(
            self, "Confirmar",
            f"¿Eliminar '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            producto_id = int(self.tabla.item(fila, 0).text())
            self.dao.eliminar(producto_id)
            self._limpiar_formulario()
            self.cargar_tabla()