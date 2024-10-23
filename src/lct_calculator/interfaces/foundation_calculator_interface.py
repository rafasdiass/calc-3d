from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QComboBox, QVBoxLayout, QProgressBar, QMessageBox, QWidget, QFrame
from PySide6.QtCore import Qt
import logging
from src.lct_calculator.calculators.foundation_calculator import FoundationCalculator
from src.lct_calculator.helpers.file_helper import FileHelper

# Configuração do logger
logging.basicConfig(level=logging.INFO)

class FoundationCalculatorInterface(QMainWindow):
    """Interface gráfica para o cálculo de fundações"""

    def __init__(self):
        super(FoundationCalculatorInterface, self).__init__()
        self.arquivo_selecionado = None
        self.tipo_fundacao_selecionada = None
        self.initUI()

    def initUI(self):
        """Inicializa a interface gráfica"""

        # Configurações principais da janela
        self.setWindowTitle('Calculadora de Fundações')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            color: #333;
            font-family: Arial, sans-serif;
            font-size: 12pt;
        """)

        # Criação do layout principal
        central_widget = QWidget()
        layout_principal = QVBoxLayout(central_widget)

        # Título
        titulo = QLabel('Calculadora de Fundações')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #0055a5;
            margin-bottom: 20px;
        """)
        layout_principal.addWidget(titulo)

        # Botão para selecionar o arquivo
        fileButton = QPushButton('Selecionar Arquivo', self)
        fileButton.clicked.connect(self.selecionar_arquivo)
        fileButton.setStyleSheet("""
            background-color: #0055a5;
            color: white;
            font-weight: bold;
            padding: 10px;
        """)
        layout_principal.addWidget(fileButton)

        # Label para exibir o caminho do arquivo selecionado
        self.label_arquivo = QLabel('Nenhum arquivo selecionado.')
        self.label_arquivo.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_arquivo.setStyleSheet("padding: 5px;")
        layout_principal.addWidget(self.label_arquivo)

        # Dropdown para selecionar o tipo de fundação
        label_fundacao = QLabel('Tipo de Fundação:')
        layout_principal.addWidget(label_fundacao)
        self.combo_tipo_fundacao = QComboBox(self)
        self.combo_tipo_fundacao.addItems([
            'Sapata', 'Bloco', 'Tubulão', 'Estaca', 'Radier',
            'Barrete', 'Sapata Corrida', 'Estaca Hélice Contínua',
            'Tubulão Céu Aberto', 'Tubulão Sob Ar Comprimido'
        ])
        self.combo_tipo_fundacao.currentTextChanged.connect(self.selecionar_tipo_fundacao)
        self.combo_tipo_fundacao.setStyleSheet("""
            background-color: white;
            padding: 5px;
        """)
        layout_principal.addWidget(self.combo_tipo_fundacao)

        # Barra de progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #0055a5;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0055a5;
                width: 10px;
            }
        """)
        layout_principal.addWidget(self.progress_bar)

        # Botão de cálculo
        calcButton = QPushButton('Calcular Fundação', self)
        calcButton.clicked.connect(self.calcular_fundacao)
        calcButton.setStyleSheet("""
            background-color: #28a745;
            color: white;
            font-weight: bold;
            padding: 10px;
        """)
        layout_principal.addWidget(calcButton)

        # Label para exibir o resultado do cálculo
        self.label_resultado = QLabel('Resultados aparecerão aqui.')
        self.label_resultado.setAlignment(Qt.AlignTop)
        self.label_resultado.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_resultado.setStyleSheet("""
            padding: 10px;
            background-color: white;
        """)
        layout_principal.addWidget(self.label_resultado)

        # Aplicando layout principal
        self.setCentralWidget(central_widget)
        self.show()

    def selecionar_arquivo(self):
        """Abre um diálogo para seleção de arquivo e exibe o arquivo selecionado"""
        arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo", "", "FreeCAD Files (*.fcstd *.ifc);;Todos os Arquivos (*)")
        if arquivo_selecionado:
            self.arquivo_selecionado = arquivo_selecionado
            self.label_arquivo.setText(f"Arquivo Selecionado: {arquivo_selecionado}")
            logging.info(f"Arquivo selecionado: {arquivo_selecionado}")
        else:
            self.label_arquivo.setText("Nenhum arquivo selecionado.")
            logging.warning("Nenhum arquivo foi selecionado.")

    def selecionar_tipo_fundacao(self, tipo_fundacao: str):
        """Armazena o tipo de fundação selecionado"""
        self.tipo_fundacao_selecionada = tipo_fundacao
        logging.info(f"Tipo de Fundação Selecionado: {tipo_fundacao}")

    def calcular_fundacao(self):
        """Inicia o processo de cálculo da fundação"""
        if self.arquivo_selecionado and self.tipo_fundacao_selecionada:
            self.progress_bar.setValue(20)
            try:
                # Carrega dados do arquivo e executa o cálculo
                dados = FileHelper.carregar_dados(self.arquivo_selecionado)
                resultado = FoundationCalculator.calcular(self.tipo_fundacao_selecionada, dados)
                self.progress_bar.setValue(100)
                self.label_resultado.setText(f"Cálculo concluído com sucesso! Resultado: {resultado}")
                logging.info("Cálculo concluído com sucesso!")
            except Exception as e:
                self.progress_bar.setValue(0)
                QMessageBox.warning(self, "Erro", f"Erro no cálculo: {e}")
                logging.error(f"Erro no cálculo: {e}")
        else:
            QMessageBox.warning(self, "Erro", "Nenhum arquivo ou tipo de fundação foi selecionado.")
            logging.warning("Tentativa de cálculo sem seleção de arquivo ou tipo de fundação.")

