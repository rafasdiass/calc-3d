from typing import Dict, Union


class ReportData:
    """
    Representa os dados gerados para o relatório de cálculo da fundação.
    Migrado de src/lct_calculator/models/report_data.py → core/models/.
    """

    def __init__(
        self,
        fundacao: Dict[str, Union[str, float]],
        resultado: float,
        conclusao: str,
    ) -> None:
        self.fundacao = fundacao
        self.resultado = resultado
        self.conclusao = conclusao

    def to_dict(self) -> Dict[str, Union[str, float, Dict[str, Union[str, float]]]]:
        return {
            "fundacao": self.fundacao,
            "resultado": self.resultado,
            "conclusao": self.conclusao,
        }
