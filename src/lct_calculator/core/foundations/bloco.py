from typing import Dict
import math

class Bloco:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Bloco.
    """

    def __init__(self, carga: float, fck: float, largura: float, comprimento: float, altura: float):
        """
        Inicializa uma instância da fundação Bloco.

        :param carga: Carga aplicada no bloco (kN)
        :param fck: Resistência característica do concreto (MPa)
        :param largura: Largura do bloco (m)
        :param comprimento: Comprimento do bloco (m)
        :param altura: Altura do bloco (m)
        """
        self.carga = carga
        self.fck = fck
        self.largura = largura
        self.comprimento = comprimento
        self.altura = altura

    def calcular_area(self) -> float:
        """
        Calcula a área do bloco (m²).

        :return: Área do bloco (m²)
        """
        return self.largura * self.comprimento

    def calcular_tensao_solo(self) -> float:
        """
        Calcula a tensão no solo (kN/m²) de acordo com a carga aplicada e a área do bloco.

        :return: Tensão no solo (kN/m²)
        """
        area = self.calcular_area()
        tensao = self.carga / area
        return tensao

    def calcular_volume_concreto(self) -> float:
        """
        Calcula o volume de concreto do bloco (m³).

        :return: Volume de concreto (m³)
        """
        volume = self.largura * self.comprimento * self.altura
        return volume

    def calcular_armacao(self) -> Dict[str, float]:
        """
        Calcula a armadura necessária para o bloco.

        :return: Dicionário com os resultados da armadura (quantidade e diâmetro)
        """
        # Exemplo de cálculo simples de armadura com base em tensões admissíveis
        armadura_minima = 0.0020  # Proporção mínima de aço para bloco
        area_aco = armadura_minima * self.calcular_area()  # Área necessária de aço (cm²)

        # Assumindo barras de aço de 12 mm
        diametro_barras = 12 / 1000  # 12 mm em metros
        area_barra = (math.pi * diametro_barras ** 2) / 4  # Área de uma barra (m²)

        quantidade_barras = area_aco / area_barra  # Número de barras necessárias

        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000  # Converter para mm
        }

    def gerar_relatorio(self) -> Dict[str, float]:
        """
        Gera um relatório com todos os cálculos do bloco.

        :return: Dicionário contendo os resultados dos cálculos
        """
        return {
            "Área do Bloco (m²)": self.calcular_area(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_solo(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Armadura - Quantidade de Barras": self.calcular_armacao()["quantidade_barras"],
            "Armadura - Diâmetro das Barras (mm)": self.calcular_armacao()["diametro_barras"]
        }
