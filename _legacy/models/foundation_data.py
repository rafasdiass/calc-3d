from typing import List, Dict, Union

class FoundationData:
    """
    Classe que representa os dados de uma fundação. Armazena informações essenciais sobre dimensões, tipo e materiais.
    """

    def __init__(self, tipo: str, largura: float, comprimento: float, altura: float, material: str):
        """
        Inicializa os dados da fundação.
        :param tipo: Tipo da fundação (ex: Sapata, Estaca, Radier, etc.).
        :param largura: Largura da fundação em metros.
        :param comprimento: Comprimento da fundação em metros.
        :param altura: Altura da fundação em metros.
        :param material: Material utilizado na fundação (ex: Concreto, Aço).
        """
        self.tipo = tipo
        self.largura = largura
        self.comprimento = comprimento
        self.altura = altura
        self.material = material

    def calcular_volume(self) -> float:
        """
        Calcula o volume da fundação com base em suas dimensões.
        :return: Volume da fundação em metros cúbicos.
        """
        return self.largura * self.comprimento * self.altura

    def to_dict(self) -> Dict[str, Union[str, float]]:
        """
        Retorna os dados da fundação em formato de dicionário.
        :return: Dicionário com as informações da fundação.
        """
        return {
            "tipo": self.tipo,
            "largura": self.largura,
            "comprimento": self.comprimento,
            "altura": self.altura,
            "material": self.material,
            "volume": self.calcular_volume()
        }
