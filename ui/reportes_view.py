from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QLineEdit,
    QPushButton, QLabel, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from database.producto_dao import ProductoDAO
from database.venta_dao import VentaDAO

class  ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ReportesView")
        self.dao_venta = VentaDAO()
        self.dao = ProductoDAO()
        self._construir_ui()
        
    def _construir_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Columna Central
        col_cen = QVBoxLayout()
        col_cen.setAlignment(Qt.AlignCenter)
        
        # Nombre de Tabla
        titulo_cen = QLabel("Detalle Venta")
        titulo_cen.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        col_cen.addWidget(titulo_cen)
        
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar Venta...")
        self.busqueda.textChanged.connect(self._filtrar_ventas)
        
        self.lista_venta = QTableWidget()
        self.lista_venta.setColumnCount(3)
        self.lista_venta.setHorizontalHeaderLabels(
            ["ID" , "Total" , "Fecha"]
        )
        self.lista_venta.horizontalHeader().setStretchLastSection(True)
        self.lista_venta.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lista_venta.setSelectionBehavior(QTableWidget.SelectRows)
        self.lista_venta.setSelectionMode(QTableWidget.SingleSelection)
        self.lista_venta.setColumnHidden(0,True)
        col_cen.addWidget(self.lista_venta)
        
        layout.addLayout(col_cen , stretch= 2)
        
    # ────────── LOGICA ──────────
    
    def _mostrar_evento(self,event):
        super().showEvent(event)
        self._cargar_ventas()

    def _cargar_ventas(self):
        ventas = self.dao_venta.obtener_todas()
        self._probar_lista(ventas)

    def _filtrar_ventas(self, texto):
        if texto.strip() == "":
            ventas = self.dao_venta.obtener_todas()
        else:
            ventas = self.dao_venta.obtener_todas()
            
    
    # ──────── Diseño ────────
    
    def _aplicar_estilos(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#ReportesView {
                background-color #ffffff;
            }
            QLabel {
                background-color: transparent;
                font-size: 13px;
                color: #ffffff;
            }"""
            
        )
    