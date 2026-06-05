from typing import Dict
import math


class Tubulao:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Tubulão.
    Nota: arquivo renomeado de tubulão.py → tubulao.py (ADR B-002: nomes de arquivo ASCII-only).
    """

    def __init__(
        self,
        carga: float,
        fck: float,
        diametro: float,
        altura: float,
        tipo: str,
        escavacao_prof: float,
        profundidade_agua: float,
    ) -> None:
        self.carga = carga
        self.fck = fck
        self.diametro = diametro
        self.altura = altura
        self.tipo = tipo
        self.escavacao_prof = escavacao_prof
        self.profundidade_agua = profundidade_agua

    def calcular_area(self) -> float:
        raio = self.diametro / 2
        return math.pi * raio ** 2

    def calcular_volume_concreto(self) -> float:
        return self.calcular_area() * self.altura

    def calcular_tensao_no_solo(self) -> float:
        return self.carga / self.calcular_area()

    def calcular_escavacao(self) -> float:
        return self.calcular_area() * self.escavacao_prof

    def calcular_pressao_lateral(self) -> float:
        densidade_agua = 1000  # kg/m³
        gravidade = 9.81  # m/s²
        return self.profundidade_agua * densidade_agua * gravidade / 1000

    def calcular_armacao(self) -> Dict[str, float]:
        armadura_minima = 0.0015
        area_aco = armadura_minima * self.calcular_area()
        diametro_barras = 16 / 1000
        area_barra = (math.pi * diametro_barras ** 2) / 4
        quantidade_barras = area_aco / area_barra
        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000,
        }

    def gerar_relatorio(self) -> Dict[str, float]:
        return {
            "Área da Base (m²)": self.calcular_area(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Volume de Escavação (m³)": self.calcular_escavacao(),
            "Pressão Lateral da Água (kN/m²)": self.calcular_pressao_lateral(),
            "Armadura - Quantidade de Barras": self.calcular_armacao()["quantidade_barras"],
            "Armadura - Diâmetro das Barras (mm)": self.calcular_armacao()["diametro_barras"],
        }
