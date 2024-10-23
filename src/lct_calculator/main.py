from src.lct_calculator.interfaces.foundation_calculator_interface import FoundationCalculatorInterface
from PySide6.QtWidgets import QApplication
import sys
import logging

# Configurando o logger
logging.basicConfig(level=logging.INFO)

def main():
    """Ponto de entrada principal da aplicação"""
    # Cria a aplicação Qt
    app = QApplication(sys.argv)
    
    # Inicializa a interface gráfica
    interface = FoundationCalculatorInterface()
    interface.show()

    # Executa a aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
