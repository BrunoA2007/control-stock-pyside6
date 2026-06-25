from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.productos_view import ProductosView
from ui.caja_view import CajaView
from ui.reportes_view import ReportesView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control de Stock y Caja")
        self.setMinimumSize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # HBoxLayout: ahora los elementos van lado a lado (horizontal)
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar (columna izquierda)
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        # Stack de páginas (columna derecha)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Páginas placeholder (por ahora solo labels)
        self.stack.addWidget(self._pagina("Inicio"))        # índice 0
        self.stack.addWidget(ProductosView())               # índice 1
        self.stack.addWidget(CajaView())                    # índice 2
        self.stack.addWidget(ReportesView())     # índice 3
        self.stack.addWidget(self._pagina("Configuracion")) # índice 4
        
        # Conectar señales de los botones a los slots
        self.sidebar.btn_inicio.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )
        self.sidebar.btn_productos.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )
        self.sidebar.btn_caja.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )
        self.sidebar.btn_reportes.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )
        self.sidebar.btn_config.clicked.connect(
            lambda: self.stack.setCurrentIndex(4)
        )


    def _pagina(self, nombre):
        """Crea una página placeholder con un label centrado."""
        pagina = QWidget()
        layout = QHBoxLayout(pagina)
        label = QLabel(f"Página: {nombre}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return pagina