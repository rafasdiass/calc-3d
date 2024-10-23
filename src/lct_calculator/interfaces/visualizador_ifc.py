import ifcopenshell
import ifcopenshell.geom
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.Qt3DExtras import Qt3DWindow, QOrbitCameraController, QPhongMaterial, QCylinderMesh
from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.QtGui import QVector3D
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)

class IFCViewer(QMainWindow):
    """Classe responsável por visualizar arquivos IFC e manipular a viewport 3D"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador IFC")
        self.setGeometry(100, 100, 1024, 768)
        self.ifc_model = None
        self.view3D = None
        self.initUI()

    def initUI(self):
        """Inicializa a interface gráfica"""

        # Configurações da interface
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Botão para carregar arquivo IFC
        self.load_button = QPushButton("Carregar Arquivo IFC", self)
        self.load_button.clicked.connect(self.carregar_arquivo)
        layout.addWidget(self.load_button)

        # Label para exibir o nome do arquivo carregado
        self.file_label = QLabel('Nenhum arquivo carregado.', self)
        layout.addWidget(self.file_label)

        # Dropdown para selecionar a fundação dentro do arquivo
        self.foundation_selector = QComboBox(self)
        layout.addWidget(self.foundation_selector)

        # Renderização 3D - área onde o modelo IFC será exibido
        self.view3D = self.setup_view_3d()
        layout.addWidget(self.view3D)

        # Setando o layout central
        self.setCentralWidget(central_widget)

    def carregar_arquivo(self):
        """Carrega o arquivo IFC e inicializa a renderização"""
        file_dialog = QFileDialog.getOpenFileName(self, "Selecionar Arquivo IFC", "", "IFC Files (*.ifc)")
        arquivo = file_dialog[0]
        if arquivo:
            self.file_label.setText(f"Arquivo Carregado: {arquivo}")
            logging.info(f"Carregando arquivo IFC: {arquivo}")

            # Carrega o arquivo IFC e processa suas fundações
            self.ifc_model = ifcopenshell.open(arquivo)
            self.preparar_fundacoes()

    def preparar_fundacoes(self):
        """Prepara os elementos de fundação para renderização e interação"""
        if self.ifc_model:
            fundacoes = self.ifc_model.by_type("IfcFooting")
            self.foundation_selector.clear()
            for fundacao in fundacoes:
                self.foundation_selector.addItem(f"{fundacao.Name} - {fundacao.GlobalId}", fundacao.GlobalId)

            if len(fundacoes) > 0:
                self.renderizar_modelo()  # Renderiza a fundação

    def renderizar_modelo(self):
        """Renderiza o modelo IFC carregado na visualização 3D"""
        if not self.ifc_model:
            return

        root_entity = QEntity()

        # Exemplo de geometria simples (um cilindro)
        cylinder = QCylinderMesh()
        cylinder.setRadius(1)
        cylinder.setLength(3)

        cylinder_entity = QEntity(root_entity)
        cylinder_entity.addComponent(cylinder)

        # Transformação e material
        cylinder_transform = QTransform()
        cylinder_entity.addComponent(cylinder_transform)

        cylinder_material = QPhongMaterial()
        cylinder_material.setDiffuse(Qt.GlobalColor.green)
        cylinder_entity.addComponent(cylinder_material)

        # Atualizando a cena com o modelo
        self.view3D.setRootEntity(root_entity)

    def setup_view_3d(self):
        """Configura a janela 3D para exibir o modelo"""
        # Configuração do Qt3D Window
        view = Qt3DWindow()
        container = self.createWindowContainer(view)
        container.setMinimumSize(800, 600)

        root_entity = QEntity()

        # Configurações da câmera
        camera = view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000)
        camera.setPosition(QVector3D(0, 0, 10))
        camera.setViewCenter(QVector3D(0, 0, 0))

        # Controlador de câmera
        camera_controller = QOrbitCameraController(root_entity)
        camera_controller.setLinearSpeed(50)
        camera_controller.setLookSpeed(180)
        camera_controller.setCamera(camera)

        view.setRootEntity(root_entity)

        return container


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    viewer = IFCViewer()
    viewer.show()
    sys.exit(app.exec())
