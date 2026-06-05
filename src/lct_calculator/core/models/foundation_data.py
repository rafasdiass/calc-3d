from typing import Dict, Union


class FoundationData:
    """
    Representa os dados de uma fundação.
    Migrado de src/lct_calculator/models/foundation_data.py → core/models/.
    """

    def __init__(
        self,
        tipo: str,
        largura: float,
        comprimento: float,
        altura: float,
        material: str,
    ) -> None:
        self.tipo = tipo
        self.largura = largura
        self.comprimento = comprimento
        self.altura = altura
        self.material = material

    def calcular_volume(self) -> float:
        return self.largura * self.comprimento * self.altura

    def to_dict(self) -> Dict[str, Union[str, float]]:
        return {
            "tipo": self.tipo,
            "largura": self.largura,
            "comprimento": self.comprimento,
            "altura": self.altura,
            "material": self.material,
            "volume": self.calcular_volume(),
        }
