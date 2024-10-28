# ifc_handler.py
import ifcopenshell
import logging

logging.basicConfig(level=logging.INFO)

class IFCHandler:
    """Classe para carregar e manipular arquivos IFC"""

    def __init__(self):
        self.ifc_model = None

    def carregar_arquivo(self, caminho_arquivo):
        """Carrega um arquivo IFC e prepara os dados"""
        try:
            self.ifc_model = ifcopenshell.open(caminho_arquivo)
            logging.info(f"Arquivo IFC {caminho_arquivo} carregado com sucesso.")
            return True
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo IFC: {e}")
            return False

    def obter_fundacoes(self):
        """Retorna uma lista de fundações no arquivo IFC"""
        if not self.ifc_model:
            return []
        return self.ifc_model.by_type("IfcFooting")
