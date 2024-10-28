# main.py
from PyQt6.QtWidgets import QApplication
import sys
from main_interface import MainInterface

def main():
    """Ponto de entrada principal da aplicação"""
    app = QApplication(sys.argv)
    interface = MainInterface()
    interface.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
