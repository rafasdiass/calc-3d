from typing import Dict
import math

class TubulaoArComprimido:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Tubulão Sob Ar Comprimido.
    """

    def __init__(self, carga: float, fck: float, diametro: float, profundidade: float, capacidade_solo: float, pressao_ar: float, peso_concreto: float = 25):
        """
        Inicializa uma instância da fundação Tubulão Sob Ar Comprimido.

        :param carga: Carga total aplicada sobre o tubulão (kN)
        :param fck: Resistência característica do concreto (MPa)
        :param diametro: Diâmetro do tubulão (m)
        :param profundidade: Profundidade do tubulão (m)
        :param capacidade_solo: Capacidade de carga do solo (kN/m²)
        :param pressao_ar: Pressão aplicada pelo ar comprimido na escavação (kPa)
        :param peso_concreto: Peso específico do concreto (kN/m³) - padrão: 25 kN/m³
        """
        self.carga = carga
        self.fck = fck
        self.diametro = diametro
        self.profundidade = profundidade
        self.capacidade_solo = capacidade_solo
        self.pressao_ar = pressao_ar
        self.peso_concreto = peso_concreto

    def calcular_area_base(self) -> float:
        """
        Calcula a área da base do tubulão (m²).

        :return: Área da base (m²)
        """
        return math.pi * (self.diametro / 2) ** 2

    def calcular_volume_concreto(self) -> float:
        """
        Calcula o volume de concreto necessário para o tubulão (m³).

        :return: Volume de concreto (m³)
        """
        return self.calcular_area_base() * self.profundidade

    def calcular_peso_concreto(self) -> float:
        """
        Calcula o peso total do concreto do tubulão (kN).

        :return: Peso do concreto (kN)
        """
        return self.calcular_volume_concreto() * self.peso_concreto

    def calcular_tensao_no_solo(self) -> float:
        """
        Calcula a tensão no solo com base na carga aplicada sobre o tubulão.

        :return: Tensão no solo (kN/m²)
        """
        return self.carga / self.calcular_area_base()

    def calcular_pressao_efetiva(self) -> float:
        """
        Calcula a pressão efetiva no solo, considerando a pressão do ar comprimido na escavação.

        :return: Pressão efetiva no solo (kN/m²)
        """
        return self.calcular_tensao_no_solo() - self.pressao_ar

    def calcular_carga_admissivel(self) -> float:
        """
        Calcula a carga admissível do tubulão com base na capacidade do solo e na pressão do ar comprimido.

        :return: Carga admissível (kN)
        """
        return self.capacidade_solo * self.calcular_area_base()

    def verificar_ruptura_solo(self) -> bool:
        """
        Verifica se há risco de ruptura do solo.

        :return: True se houver risco de ruptura, False caso contrário.
        """
        return self.carga > self.calcular_carga_admissivel()

    def calcular_armacao_longitudinal(self) -> Dict[str, float]:
        """
        Calcula a armadura longitudinal necessária para o tubulão.

        :return: Dicionário com a quantidade de aço e o diâmetro das barras
        """
        armadura_minima = 0.0025  # Proporção mínima de aço para tubulão (0,25%)
        area_aco = armadura_minima * math.pi * (self.diametro / 2) ** 2  # Área de aço longitudinal necessária (m²)

        # Supondo barras de 20 mm de diâmetro
        diametro_barras = 20 / 1000  # 20 mm em metros
        area_barra = (math.pi * diametro_barras ** 2) / 4  # Área de uma barra (m²)

        quantidade_barras = area_aco / area_barra  # Número de barras necessárias

        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000  # Convertendo para mm
        }

    def calcular_armacao_transversal(self) -> Dict[str, float]:
        """
        Calcula a armadura transversal (estribos) necessária para o tubulão.

        :return: Dicionário com a quantidade de estribos e o diâmetro das barras
        """
        armadura_minima = 0.0015  # Proporção mínima de aço para estribos (0,15%)
        area_aco_transversal = armadura_minima * self.diametro * self.profundidade  # Área de aço transversal necessária (m²)

        # Supondo barras de 12 mm de diâmetro para estribos
        diametro_estribos = 12 / 1000  # 12 mm em metros
        area_estribo = (math.pi * diametro_estribos ** 2) / 4  # Área de um estribo (m²)

        quantidade_estribos = area_aco_transversal / area_estribo  # Número de estribos necessários

        return {
            "quantidade_estribos": quantidade_estribos,
            "diametro_estribos": diametro_estribos * 1000  # Convertendo para mm
        }

    def calcular_assentamento_solo(self) -> float:
        """
        Calcula o assentamento esperado do solo com base na tensão aplicada e nas propriedades do solo.
        O assentamento depende da compressibilidade do solo e das tensões aplicadas.

        :return: Assentamento estimado (mm)
        """
        modulo_deformacao = 15000  # Valor típico em kN/m² para solos firmes
        tensao_no_solo = self.calcular_tensao_no_solo()
        assentamento = (tensao_no_solo / modulo_deformacao) * self.profundidade * 1000  # Convertendo para mm
        return assentamento

    def gerar_relatorio(self) -> Dict[str, float]:
        """
        Gera um relatório completo com os cálculos do tubulão.

        :return: Dicionário contendo os resultados dos cálculos
        """
        return {
            "Área da Base (m²)": self.calcular_area_base(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Peso do Concreto (kN)": self.calcular_peso_concreto(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Pressão Efetiva no Solo (kN/m²)": self.calcular_pressao_efetiva(),
            "Carga Admissível (kN)": self.calcular_carga_admissivel(),
            "Ruptura do Solo": self.verificar_ruptura_solo(),
            "Armadura Longitudinal - Quantidade de Barras": self.calcular_armacao_longitudinal()["quantidade_barras"],
            "Armadura Longitudinal - Diâmetro das Barras (mm)": self.calcular_armacao_longitudinal()["diametro_barras"],
            "Armadura Transversal - Quantidade de Estribos": self.calcular_armacao_transversal()["quantidade_estribos"],
            "Armadura Transversal - Diâmetro dos Estribos (mm)": self.calcular_armacao_transversal()["diametro_estribos"],
            "Assentamento Estimado do Solo (mm)": self.calcular_assentamento_solo()
        }
