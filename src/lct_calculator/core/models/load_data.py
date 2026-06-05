from typing import Dict


class LoadData:
    """
    Representa os dados de cargas aplicadas à fundação.
    Migrado de src/lct_calculator/models/load_data.py → core/models/.
    """

    def __init__(
        self,
        carga_axial: float,
        momento_fletor: float,
        cisalhamento: float,
    ) -> None:
        self.carga_axial = carga_axial
        self.momento_fletor = momento_fletor
        self.cisalhamento = cisalhamento

    def to_dict(self) -> Dict[str, float]:
        return {
            "carga_axial": self.carga_axial,
            "momento_fletor": self.momento_fletor,
            "cisalhamento": self.cisalhamento,
        }
