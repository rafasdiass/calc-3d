from typing import List, Dict

class LoadData:
    """
    Classe que representa os dados de cargas aplicadas à fundação.
    """

    def __init__(self, carga_axial: float, momento_fletor: float, cisalhamento: float):
        """
        Inicializa os dados de carga aplicados à fundação.
        :param carga_axial: Carga axial aplicada (kN).
        :param momento_fletor: Momento fletor aplicado (kNm).
        :param cisalhamento: Força de cisalhamento aplicada (kN).
        """
        self.carga_axial = carga_axial
        self.momento_fletor = momento_fletor
        self.cisalhamento = cisalhamento

    def to_dict(self) -> Dict[str, float]:
        """
        Retorna os dados de carga em formato de dicionário.
        :return: Dicionário com as informações de carga.
        """
        return {
            "carga_axial": self.carga_axial,
            "momento_fletor": self.momento_fletor,
            "cisalhamento": self.cisalhamento
        }
