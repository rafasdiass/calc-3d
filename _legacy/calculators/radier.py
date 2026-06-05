from typing import Dict
import math

class Radier:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Radier.
    """

    def __init__(self, carga_total: float, fck: float, area: float, espessura: float, capacidade_solo: float, peso_concreto: float = 25):
        """
        Inicializa uma instância da fundação Radier.

        :param carga_total: Carga total aplicada sobre o radier (kN)
        :param fck: Resistência característica do concreto (MPa)
        :param area: Área do radier (m²)
        :param espessura: Espessura da laje do radier (m)
        :param capacidade_solo: Capacidade de carga do solo (kN/m²)
        :param peso_concreto: Peso específico do concreto (kN/m³) - padrão: 25 kN/m³
        """
        self.carga_total = carga_total
        self.fck = fck
        self.area = area
        self.espessura = espessura
        self.capacidade_solo = capacidade_solo
        self.peso_concreto = peso_concreto

    def calcular_volume_concreto(self) -> float:
        """
        Calcula o volume de concreto necessário para o radier (m³).

        :return: Volume de concreto (m³)
        """
        return self.area * self.espessura

    def calcular_peso_concreto(self) -> float:
        """
        Calcula o peso total do concreto do radier (kN).

        :return: Peso do concreto (kN)
        """
        return self.calcular_volume_concreto() * self.peso_concreto

    def calcular_tensao_no_solo(self) -> float:
        """
        Calcula a tensão no solo com base na carga aplicada.

        :return: Tensão no solo (kN/m²)
        """
        return self.carga_total / self.area

    def calcular_carga_admissivel(self) -> float:
        """
        Calcula a carga admissível do radier com base na capacidade do solo.

        :return: Carga admissível (kN)
        """
        return self.capacidade_solo * self.area

    def verificar_ruptura_solo(self) -> bool:
        """
        Verifica se há risco de ruptura do solo.

        :return: True se houver risco de ruptura, False caso contrário.
        """
        return self.carga_total > self.calcular_carga_admissivel()

    def calcular_armacao(self) -> Dict[str, float]:
        """
        Calcula a armadura necessária para o radier.

        :return: Dicionário com a quantidade de aço e o diâmetro das barras
        """
        armadura_minima = 0.0015  # Proporção mínima de aço para radier (0,15%)
        area_aco = armadura_minima * self.area * self.espessura  # Área de aço necessária (m²)

        # Supondo barras de 10 mm de diâmetro
        diametro_barras = 10 / 1000  # 10 mm em metros
        area_barra = (math.pi * diametro_barras ** 2) / 4  # Área de uma barra (m²)

        quantidade_barras = area_aco / area_barra  # Número de barras necessárias

        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000  # Convertendo para mm
        }

    def gerar_relatorio(self) -> Dict[str, float]:
        """
        Gera um relatório completo com os cálculos do radier.

        :return: Dicionário contendo os resultados dos cálculos
        """
        return {
            "Área (m²)": self.area,
            "Espessura (m)": self.espessura,
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Peso do Concreto (kN)": self.calcular_peso_concreto(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Carga Admissível (kN)": self.calcular_carga_admissivel(),
            "Ruptura do Solo": self.verificar_ruptura_solo(),
            "Armadura - Quantidade de Barras": self.calcular_armacao()["quantidade_barras"],
            "Armadura - Diâmetro das Barras (mm)": self.calcular_armacao()["diametro_barras"]
        }
