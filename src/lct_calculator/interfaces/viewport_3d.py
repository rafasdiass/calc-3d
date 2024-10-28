# viewport_3d.py
from PyQt6.Qt3DExtras import Qt3DWindow, QOrbitCameraController
from PyQt6.Qt3DCore import QEntity
from PyQt6.QtGui import QVector3D

class Viewport3D:
    def __init__(self):
        self.view = Qt3DWindow()
        self.root_entity = QEntity()
        self.view.setRootEntity(self.root_entity)
        self.setup_camera()

    def setup_camera(self):
        """Configura a câmera e controlador de câmera na viewport."""
        camera = self.view.camera()
        camera.setPosition(QVector3D(0, 10, 20))
        camera.setViewCenter(QVector3D(0, 0, 0))
        
        # Controlador de câmera
        camera_controller = QOrbitCameraController(self.root_entity)
        camera_controller.setCamera(camera)

    def get_container(self):
        """Retorna o container da janela 3D para inserção na interface principal."""
        return self.view.createWindowContainer()
