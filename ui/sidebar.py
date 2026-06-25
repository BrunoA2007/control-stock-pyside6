from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(180)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(4)
        layout.setContentsMargins(12, 20, 12, 20)

        # Título del sidebar
        titulo = QLabel("Maria Shop")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px 0px;")
        layout.addWidget(titulo)

        # Creamos los botones
        self.btn_inicio    = self._crear_boton("Inicio")
        self.btn_productos = self._crear_boton("Productos")
        self.btn_caja      = self._crear_boton("Caja")
        self.btn_reportes  = self._crear_boton("Reportes")
        self.btn_config    = self._crear_boton("Configuración")

        self._botones = [
            self.btn_inicio, self.btn_productos,
            self.btn_caja, self.btn_reportes, self.btn_config
        ]

        for btn in self._botones:
            layout.addWidget(btn)

        # Aplicar estilos a todo el sidebar
        self._aplicar_estilos()

        # El botón de inicio empieza activo
        self.btn_inicio.setChecked(True)

    def _crear_boton(self, texto):
        """Crea un botón de navegación checkable."""
        btn = QPushButton(texto)
        btn.setFixedHeight(42)
        btn.setCheckable(True)  # ← habilita el estado :checked
        # Al clickear uno, desactivamos todos los demás
        btn.clicked.connect(lambda: self._activar_boton(btn))
        return btn

    def _activar_boton(self, boton_activo):
        """Deja solo un botón en estado checked."""
        for btn in self._botones:
            btn.setChecked(btn is boton_activo)

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #303238;
            }

            QPushButton {
                background-color: transparent;
                color: #a0a8c0;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #3a3f52;
                color: #ffffff;
            }

            QPushButton:checked {
                background-color: #4AD977;
                color: #ffffff;
                font-weight: bold;
            }

            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
        """)