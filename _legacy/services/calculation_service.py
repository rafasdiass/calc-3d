from typing import Dict, Any
from src.lct_calculator.calculators import (
    Sapata, Bloco, Tubulão, Estaca, Radier, Barrete, SapataCorrida,
    EstacaHeliceContinua, TubulãoCéuAberto, TubulãoSobArComprimido
)
from src.lct_calculator.models.foundation_data import FoundationData
from src.lct_calculator.models.load_data import LoadData
from src.lct_calculator.models.report_data import ReportData
import logging

# Configurando o logger
logging.basicConfig(level=logging.INFO)

class CalculationService:
    """
    Classe responsável por gerenciar o cálculo de fundações.
    Ela orquestra o processo de seleção do tipo de fundação correto
    e invoca o cálculo apropriado.
    """

    def __init__(self):
        self.calculators = {
            'sapata': Sapata(),
            'bloco': Bloco(),
            'tubulão': Tubulão(),
            'estaca': Estaca(),
            'radier': Radier(),
            'barrete': Barrete(),
            'sapata_corrida': SapataCorrida(),
            'estaca_helice_continua': EstacaHeliceContinua(),
            'tubulão_céu_aberto': TubulãoCéuAberto(),
            'tubulão_sob_ar_comprimido': TubulãoSobArComprimido(),
        }

    def calcular_fundacao(
        self, tipo_fundacao: str, foundation_data: FoundationData, load_data: LoadData
    ) -> ReportData:
        """
        Realiza o cálculo da fundação com base no tipo especificado e nos dados fornecidos.
        
        Args:
            tipo_fundacao (str): O tipo de fundação a ser calculado (e.g., 'sapata', 'bloco').
            foundation_data (FoundationData): Dados da fundação (dimensões, material, etc.).
            load_data (LoadData): Dados das cargas aplicadas (peso, pressão, etc.).

        Returns:
            ReportData: O relatório com os resultados dos cálculos.
        """
        logging.info(f"Iniciando cálculo para fundação: {tipo_fundacao}")
        
        # Verifica se o tipo de fundação é válido
        if tipo_fundacao not in self.calculators:
            raise ValueError(f"Tipo de fundação '{tipo_fundacao}' não é suportado.")
        
        # Seleciona o calculador correto
        calculador = self.calculators[tipo_fundacao]
        
        # Executa o cálculo e retorna os resultados
        resultado = calculador.calcular(foundation_data, load_data)
        logging.info(f"Cálculo concluído para {tipo_fundacao}. Resultados: {resultado}")
        
        return resultado

# Exemplo de como utilizar a classe CalculationService
if __name__ == "__main__":
    service = CalculationService()
    
    # Mock de dados de entrada (simulando dados reais)
    foundation_data = FoundationData(tipo='sapata', largura=5.0, comprimento=4.0, altura=1.5, material='concreto')
    load_data = LoadData(carga_axial=500, momento_fletor=200, cisalhamento=150)
    
    # Executa o cálculo para uma sapata
    resultado = service.calcular_fundacao('sapata', foundation_data, load_data)
    print(f"Resultado do cálculo: {resultado}")
