# main_interface.py
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox, QComboBox
from viewport_3d import Viewport3D
from ifc_handler import IFCHandler

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora de Fundações')
        
        # Instâncias da viewport 3D e do manipulador IFC
        self.view3D = Viewport3D()
        self.ifc_handler = IFCHandler()
        
        self.initUI()

    def initUI(self):
        """Inicializa a interface gráfica principal."""
        central_widget = QWidget()
        layout_principal = QHBoxLayout(central_widget)
        
        # Layout para a visualização 3D
        layout_visualizacao = QVBoxLayout()
        layout_visualizacao.addWidget(self.view3D.get_container())

        # Layout para as ferramentas
        layout_ferramentas = QVBoxLayout()
        
        # Botão para carregar arquivo IFC
        fileButton = QPushButton('Selecionar Arquivo IFC')
        fileButton.clicked.connect(self.selecionar_arquivo)
        layout_ferramentas.addWidget(fileButton)

        # Label para exibir o nome do arquivo selecionado
        self.label_arquivo = QLabel('Nenhum arquivo selecionado.')
        layout_ferramentas.addWidget(self.label_arquivo)

        # Dropdown para selecionar fundações
        self.foundation_selector = QComboBox(self)
        layout_ferramentas.addWidget(self.foundation_selector)

        # Grupo de ferramentas
        group_box = QGroupBox("Ferramentas")
        group_box.setLayout(layout_ferramentas)

        # Adiciona os layouts ao layout principal
        layout_principal.addLayout(layout_visualizacao, 3)
        layout_principal.addWidget(group_box, 1)

        # Define o widget central da janela
        self.setCentralWidget(central_widget)

    def selecionar_arquivo(self):
        """Abre um diálogo para selecionar o arquivo IFC e carrega-o no handler."""
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo IFC", "", "IFC Files (*.ifc);;Todos os Arquivos (*)")
        if arquivo:
            self.label_arquivo.setText(f"Arquivo Selecionado: {arquivo}")
            if self.ifc_handler.carregar_arquivo(arquivo):
                self.preparar_fundacoes()

    def preparar_fundacoes(self):
        """Atualiza a lista de fundações disponíveis após carregar o arquivo IFC"""
        fundacoes = self.ifc_handler.obter_fundacoes()
        self.foundation_selector.clear()
        for fundacao in fundacoes:
            self.foundation_selector.addItem(f"{fundacao.Name} - {fundacao.GlobalId}", fundacao.GlobalId)
