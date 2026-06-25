import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.init_db import inicializar_db  # ← nuevo

def main():
    inicializar_db()  # ← crea las tablas si no existen
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()