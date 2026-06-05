from typing import Dict
import math

class Tubulao:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Tubulão.
    """

    def __init__(self, carga: float, fck: float, diametro: float, altura: float, tipo: str, escavacao_prof: float, profundidade_agua: float):
        """
        Inicializa uma instância da fundação Tubulão.

        :param carga: Carga aplicada no tubulão (kN)
        :param fck: Resistência característica do concreto (MPa)
        :param diametro: Diâmetro do tubulão (m)
        :param altura: Altura do tubulão (m)
        :param tipo: Tipo de tubulão ("Céu Aberto" ou "Sob Ar Comprimido")
        :param escavacao_prof: Profundidade da escavação (m)
        :param profundidade_agua: Profundidade do nível freático (m)
        """
        self.carga = carga
        self.fck = fck
        self.diametro = diametro
        self.altura = altura
        self.tipo = tipo
        self.escavacao_prof = escavacao_prof
        self.profundidade_agua = profundidade_agua

    def calcular_area(self) -> float:
        """
        Calcula a área da base do tubulão (m²).

        :return: Área da base (m²)
        """
        raio = self.diametro / 2
        return math.pi * raio ** 2

    def calcular_volume_concreto(self) -> float:
        """
        Calcula o volume de concreto do tubulão (m³).

        :return: Volume de concreto (m³)
        """
        return self.calcular_area() * self.altura

    def calcular_tensao_no_solo(self) -> float:
        """
        Calcula a tensão no solo (kN/m²) de acordo com a carga aplicada e a área do tubulão.

        :return: Tensão no solo (kN/m²)
        """
        area = self.calcular_area()
        return self.carga / area

    def calcular_escavacao(self) -> float:
        """
        Calcula o volume de escavação necessário para o tubulão (m³).

        :return: Volume de escavação (m³)
        """
        return self.calcular_area() * self.escavacao_prof

    def calcular_pressao_lateral(self) -> float:
        """
        Calcula a pressão lateral de água no tubulão (kN/m²) com base na profundidade da água.

        :return: Pressão lateral de água (kN/m²)
        """
        # Pressão hidrostática = profundidade * densidade da água (1000 kg/m³) * gravidade (9.81 m/s²)
        densidade_agua = 1000  # kg/m³
        gravidade = 9.81  # m/s²
        return self.profundidade_agua * densidade_agua * gravidade / 1000  # Convertendo para kN/m²

    def calcular_armacao(self) -> Dict[str, float]:
        """
        Calcula a armadura necessária para o tubulão.

        :return: Dicionário com os resultados da armadura (quantidade e diâmetro)
        """
        armadura_minima = 0.0015  # Proporção mínima de aço para tubulão (mais leve que blocos)
        area_aco = armadura_minima * self.calcular_area()  # Área de aço necessária (cm²)

        # Assumindo barras de aço de 16 mm
        diametro_barras = 16 / 1000  # 16 mm em metros
        area_barra = (math.pi * diametro_barras ** 2) / 4  # Área de uma barra (m²)

        quantidade_barras = area_aco / area_barra  # Número de barras necessárias

        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000  # Converter para mm
        }

    def gerar_relatorio(self) -> Dict[str, float]:
        """
        Gera um relatório completo com todos os cálculos do tubulão.

        :return: Dicionário contendo os resultados dos cálculos
        """
        return {
            "Área da Base (m²)": self.calcular_area(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Volume de Escavação (m³)": self.calcular_escavacao(),
            "Pressão Lateral da Água (kN/m²)": self.calcular_pressao_lateral(),
            "Armadura - Quantidade de Barras": self.calcular_armacao()["quantidade_barras"],
            "Armadura - Diâmetro das Barras (mm)": self.calcular_armacao()["diametro_barras"]
        }
