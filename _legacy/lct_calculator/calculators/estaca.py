from typing import Dict
import math

class Estaca:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Estaca.
    """

    def __init__(self, carga: float, fck: float, diametro: float, comprimento: float, capacidade_solo: float, peso_concreto: float = 25):
        """
        Inicializa uma instância da fundação Estaca.

        :param carga: Carga aplicada na estaca (kN)
        :param fck: Resistência característica do concreto (MPa)
        :param diametro: Diâmetro da estaca (m)
        :param comprimento: Comprimento da estaca (m)
        :param capacidade_solo: Capacidade de carga do solo (kN/m²)
        :param peso_concreto: Peso específico do concreto (kN/m³) - padrão: 25 kN/m³
        """
        self.carga = carga
        self.fck = fck
        self.diametro = diametro
        self.comprimento = comprimento
        self.capacidade_solo = capacidade_solo
        self.peso_concreto = peso_concreto

    def calcular_area(self) -> float:
        """
        Calcula a área da seção transversal da estaca (m²).

        :return: Área da seção transversal (m²)
        """
        raio = self.diametro / 2
        return math.pi * raio ** 2

    def calcular_volume_concreto(self) -> float:
        """
        Calcula o volume de concreto da estaca (m³).

        :return: Volume de concreto (m³)
        """
        return self.calcular_area() * self.comprimento

    def calcular_peso_concreto(self) -> float:
        """
        Calcula o peso total do concreto da estaca (kN).

        :return: Peso do concreto (kN)
        """
        return self.calcular_volume_concreto() * self.peso_concreto

    def calcular_tensao_no_solo(self) -> float:
        """
        Calcula a tensão no solo com base na carga aplicada e na capacidade de carga do solo.

        :return: Tensão no solo (kN/m²)
        """
        area = self.calcular_area()
        return self.carga / area

    def calcular_carga_admissivel(self) -> float:
        """
        Calcula a carga admissível da estaca de acordo com a capacidade do solo.

        :return: Carga admissível (kN)
        """
        return self.capacidade_solo * self.calcular_area()

    def verificar_ruptura_solo(self) -> bool:
        """
        Verifica se há risco de ruptura do solo, comparando a carga aplicada com a carga admissível do solo.

        :return: True se houver risco de ruptura, False caso contrário.
        """
        return self.carga > self.calcular_carga_admissivel()

    def calcular_armacao(self) -> Dict[str, float]:
        """
        Calcula a armadura necessária para a estaca.

        :return: Dicionário com a quantidade de barras e diâmetro
        """
        armadura_minima = 0.002  # Proporção mínima de aço para estacas (2%)
        area_aco = armadura_minima * self.calcular_area()  # Área de aço necessária (m²)

        # Assumindo barras de 20 mm
        diametro_barras = 20 / 1000  # 20 mm em metros
        area_barra = (math.pi * diametro_barras ** 2) / 4  # Área de uma barra (m²)

        quantidade_barras = area_aco / area_barra  # Número de barras necessárias

        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000  # Convertendo para mm
        }

    def gerar_relatorio(self) -> Dict[str, float]:
        """
        Gera um relatório completo com todos os cálculos da estaca.

        :return: Dicionário contendo os resultados dos cálculos
        """
        return {
            "Área da Seção Transversal (m²)": self.calcular_area(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Peso do Concreto (kN)": self.calcular_peso_concreto(),
            "Carga Admissível (kN)": self.calcular_carga_admissivel(),
            "Ruptura do Solo": self.verificar_ruptura_solo(),
            "Armadura - Quantidade de Barras": self.calcular_armacao()["quantidade_barras"],
            "Armadura - Diâmetro das Barras (mm)": self.calcular_armacao()["diametro_barras"]
        }
