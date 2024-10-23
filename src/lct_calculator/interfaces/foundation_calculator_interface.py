from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QComboBox, QVBoxLayout, QWidget, QFrame, QHBoxLayout, QTextEdit, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.Qt3DExtras import Qt3DWindow, QOrbitCameraController, QPhongMaterial, QCylinderMesh
from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.QtGui import QVector3D
import logging
import ifcopenshell
import ifcopenshell.geom

# Configuração do logger
logging.basicConfig(level=logging.INFO)

class FoundationCalculatorInterface(QMainWindow):
    """Interface gráfica para o cálculo e visualização de fundações"""

    def __init__(self):
        super(FoundationCalculatorInterface, self).__init__()
        self.arquivo_selecionado = None
        self.tipo_fundacao_selecionada = None
        self.ifc_model = None
        self.view3D = None
        self.resultado = None
        self.initUI()

    def initUI(self):
        """Inicializa a interface gráfica"""

        # Configurações principais da janela
        self.setWindowTitle('Calculadora de Fundações com Visualização')
        self.setGeometry(100, 100, 1200, 800)  # Aumenta o tamanho da janela
        self.setStyleSheet("""
            background-color: #f0f0f0;
            color: #333;
            font-family: Arial, sans-serif;
            font-size: 12pt;
        """)

        # Criação do layout principal
        central_widget = QWidget()
        layout_principal = QHBoxLayout(central_widget)  # Layout horizontal

        # Seção esquerda: Visualização 3D
        layout_visualizacao = QVBoxLayout()

        # Renderização 3D
        self.view3D = self.setup_view_3d()
        layout_visualizacao.addWidget(self.view3D)

        # Seção direita: Ferramentas e opções
        layout_ferramentas = QVBoxLayout()

        # Agrupando as ferramentas
        group_box = QGroupBox("Ferramentas")
        group_layout = QVBoxLayout()

        # Título
        titulo = QLabel('Calculadora e Visualizador de Fundações')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #0055a5;
            margin-bottom: 20px;
        """)
        group_layout.addWidget(titulo)

        # Botão para selecionar o arquivo
        fileButton = QPushButton('Selecionar Arquivo IFC', self)
        fileButton.clicked.connect(self.selecionar_arquivo)
        fileButton.setStyleSheet("""
            background-color: #0055a5;
            color: white;
            font-weight: bold;
            padding: 10px;
        """)
        group_layout.addWidget(fileButton)

        # Label para exibir o caminho do arquivo selecionado
        self.label_arquivo = QLabel('Nenhum arquivo selecionado.')
        self.label_arquivo.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.label_arquivo.setStyleSheet("padding: 5px;")
        group_layout.addWidget(self.label_arquivo)

        # Dropdown para selecionar o tipo de fundação
        label_fundacao = QLabel('Tipo de Fundação:')
        group_layout.addWidget(label_fundacao)
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
        group_layout.addWidget(self.combo_tipo_fundacao)

        # Área de resultados
        self.resultado = QTextEdit(self)
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("""
            background-color: white;
            padding: 5px;
            font-family: Arial;
        """)
        group_layout.addWidget(self.resultado)

        # Aplicando o layout de ferramentas ao GroupBox
        group_box.setLayout(group_layout)
        layout_ferramentas.addWidget(group_box)

        # Adiciona as duas seções no layout principal
        layout_principal.addLayout(layout_visualizacao, 3)  # Aumenta o peso da área de visualização
        layout_principal.addLayout(layout_ferramentas, 1)  # Ferramentas na direita com menor peso

        # Aplicando layout principal
        self.setCentralWidget(central_widget)
        self.show()

    def selecionar_arquivo(self):
        """Abre um diálogo para seleção de arquivo IFC e exibe o arquivo selecionado"""
        arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo IFC", "", "IFC Files (*.ifc);;Todos os Arquivos (*)")
        if arquivo_selecionado:
            self.arquivo_selecionado = arquivo_selecionado
            self.label_arquivo.setText(f"Arquivo Selecionado: {arquivo_selecionado}")
            logging.info(f"Arquivo selecionado: {arquivo_selecionado}")
            self.carregar_arquivo_ifc(arquivo_selecionado)
        else:
            self.label_arquivo.setText("Nenhum arquivo selecionado.")
            logging.warning("Nenhum arquivo foi selecionado.")

    def selecionar_tipo_fundacao(self, tipo_fundacao: str):
        """Armazena o tipo de fundação selecionado"""
        self.tipo_fundacao_selecionada = tipo_fundacao
        logging.info(f"Tipo de Fundação Selecionado: {tipo_fundacao}")

    def carregar_arquivo_ifc(self, arquivo):
        """Carrega o arquivo IFC e inicializa a renderização"""
        if arquivo:
            logging.info(f"Carregando arquivo IFC: {arquivo}")
            self.ifc_model = ifcopenshell.open(arquivo)
            self.renderizar_modelo()

    def renderizar_modelo(self):
        """Renderiza o modelo IFC carregado na visualização 3D"""
        if not self.ifc_model:
            return

        rootEntity = self.view3D.rootEntity()

        # Exemplo de geometria simples (um cubo representado com cilindros)
        self.create_reference_cube(rootEntity)

    def setup_view_3d(self):
        """Configura a janela 3D para exibir o modelo"""
        # Configuração do Qt3D Window
        view = Qt3DWindow()
        view.defaultFrameGraph().setClearColor(Qt.GlobalColor.lightGray)  # Fundo cinza
        container = self.createWindowContainer(view)
        container.setMinimumSize(800, 600)

        rootEntity = QEntity()

        # Adicionando um grid (plano quadriculado) na cena
        self.create_grid(rootEntity)

        # Configurações da câmera
        camera = view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000)
        camera.setPosition(QVector3D(0, 10, 20))
        camera.setViewCenter(QVector3D(0, 0, 0))

        # Controlador de câmera
        cameraController = QOrbitCameraController(rootEntity)
        cameraController.setLinearSpeed(50)
        cameraController.setLookSpeed(180)
        cameraController.setCamera(camera)

        view.setRootEntity(rootEntity)

        return container

    def create_grid(self, rootEntity):
        """Cria um grid para servir como plano de fundo na visualização 3D"""
        grid_size = 10  # Tamanho do grid
        grid_spacing = 1  # Espaçamento entre as linhas
        grid_color = Qt.GlobalColor.lightGray  # Cor do grid

        for i in range(-grid_size, grid_size + 1, grid_spacing):
            # Linhas no eixo X
            self.create_line(rootEntity, QVector3D(i, 0, -grid_size), QVector3D(i, 0, grid_size), grid_color)
            # Linhas no eixo Z
            self.create_line(rootEntity, QVector3D(-grid_size, 0, i), QVector3D(grid_size, 0, i), grid_color)

    def create_line(self, rootEntity, start, end, color):
        """Cria uma linha simples entre dois pontos no espaço 3D"""
        line_entity = QEntity(rootEntity)
        line_mesh = QCylinderMesh()
        line_mesh.setRadius(0.02)
        line_mesh.setLength((start - end).length())

        transform = QTransform()
        transform.setTranslation((start + end) / 2)

        line_material = QPhongMaterial()
        line_material.setDiffuse(color)

        line_entity.addComponent(line_mesh)
        line_entity.addComponent(transform)
        line_entity.addComponent(line_material)

    def create_reference_cube(self, rootEntity):
        """Cria um cubo manualmente utilizando cilindros para representar as arestas"""
        cube_size = 1  # Tamanho do cubo

        # Definir os 8 vértices do cubo
        vertices = [
            QVector3D(-cube_size, -cube_size, -cube_size),
            QVector3D(cube_size, -cube_size, -cube_size),
            QVector3D(cube_size, cube_size, -cube_size),
            QVector3D(-cube_size, cube_size, -cube_size),
            QVector3D(-cube_size, -cube_size, cube_size),
            QVector3D(cube_size, -cube_size, cube_size),
            QVector3D(cube_size, cube_size, cube_size),
            QVector3D(-cube_size, cube_size, cube_size),
        ]

        # Arestas do cubo (ligando os vértices)
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Face inferior
            (4, 5), (5, 6), (6, 7), (7, 4),  # Face superior
            (0, 4), (1, 5), (2, 6), (3, 7)   # Conectando faces superior e inferior
        ]

        # Cor do cubo
        cube_color = Qt.GlobalColor.blue

        # Criar cada aresta usando cilindros
        for start_idx, end_idx in edges:
            self.create_line(rootEntity, vertices[start_idx], vertices[end_idx], cube_color)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    viewer = FoundationCalculatorInterface()
    viewer.show()
    sys.exit(app.exec())
