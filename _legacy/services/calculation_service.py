import logging
from typing import Dict

from lct_calculator.calculators import (
    Sapata,
    Bloco,
    Tubulao,
    Estaca,
    Radier,
    Barrete,
    SapataCorrida,
    EstacaHeliceContinua,
    TubulaoCeuAberto,
    TubulaoArComprimido,
)
from lct_calculator.models.foundation_data import FoundationData
from lct_calculator.models.load_data import LoadData
from lct_calculator.models.report_data import ReportData

logger = logging.getLogger(__name__)


class CalculationService:
    """
    Orquestrador de cálculo de fundações.
    Seleciona o calculator correto e delega a execução.
    """

    def __init__(self) -> None:
        self.calculators: Dict[str, object] = {
            "sapata": Sapata,
            "bloco": Bloco,
            "tubulao": Tubulao,
            "estaca": Estaca,
            "radier": Radier,
            "barrete": Barrete,
            "sapata_corrida": SapataCorrida,
            "estaca_helice_continua": EstacaHeliceContinua,
            "tubulao_ceu_aberto": TubulaoCeuAberto,
            "tubulao_ar_comprimido": TubulaoArComprimido,
        }

    def calcular_fundacao(
        self,
        tipo_fundacao: str,
        foundation_data: FoundationData,
        load_data: LoadData,
    ) -> ReportData:
        """
        Realiza o cálculo da fundação com base no tipo especificado e nos dados fornecidos.

        Args:
            tipo_fundacao: Chave do tipo de fundação (ex: 'sapata', 'estaca').
            foundation_data: Dados da fundação (dimensões, material, etc.).
            load_data: Dados das cargas aplicadas.

        Returns:
            ReportData com os resultados dos cálculos.

        Raises:
            ValueError: Se o tipo de fundação não for suportado.
        """
        logger.info("Iniciando cálculo para fundação: %s", tipo_fundacao)

        if tipo_fundacao not in self.calculators:
            raise ValueError(
                f"Tipo de fundação '{tipo_fundacao}' não é suportado. "
                f"Tipos válidos: {sorted(self.calculators.keys())}"
            )

        calculador = self.calculators[tipo_fundacao]
        resultado = calculador.calcular(foundation_data, load_data)  # type: ignore[union-attr]
        logger.info("Cálculo concluído para %s.", tipo_fundacao)

        return resultado
