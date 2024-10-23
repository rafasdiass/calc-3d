from typing import Dict, Union

class ReportData:
    """
    Classe que representa os dados gerados para o relatório de cálculo da fundação.
    """

    def __init__(self, fundacao: Dict[str, Union[str, float]], resultado: float, conclusao: str):
        """
        Inicializa os dados do relatório.
        :param fundacao: Dicionário com os dados da fundação.
        :param resultado: Resultado dos cálculos (ex: capacidade de carga).
        :param conclusao: Conclusão sobre o cálculo (ex: Fundação segura, revisar dimensões).
        """
        self.fundacao = fundacao
        self.resultado = resultado
        self.conclusao = conclusao

    def to_dict(self) -> Dict[str, Union[str, float]]:
        """
        Retorna os dados do relatório em formato de dicionário.
        :return: Dicionário com as informações do relatório.
        """
        return {
            "fundacao": self.fundacao,
            "resultado": self.resultado,
            "conclusao": self.conclusao
        }
