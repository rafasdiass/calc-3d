from typing import Dict
import math


class TubulaoCeuAberto:
    """
    Classe responsável pelos cálculos de uma fundação do tipo Tubulão Céu Aberto.
    Nota: arquivo renomeado de tubulão_ceu_aberto.py → tubulao_ceu_aberto.py (ADR B-002).
    """

    def __init__(
        self,
        carga: float,
        fck: float,
        diametro: float,
        profundidade: float,
        capacidade_solo: float,
        peso_concreto: float = 25,
    ) -> None:
        self.carga = carga
        self.fck = fck
        self.diametro = diametro
        self.profundidade = profundidade
        self.capacidade_solo = capacidade_solo
        self.peso_concreto = peso_concreto

    def calcular_area_base(self) -> float:
        return math.pi * (self.diametro / 2) ** 2

    def calcular_volume_concreto(self) -> float:
        return self.calcular_area_base() * self.profundidade

    def calcular_peso_concreto(self) -> float:
        return self.calcular_volume_concreto() * self.peso_concreto

    def calcular_tensao_no_solo(self) -> float:
        return self.carga / self.calcular_area_base()

    def calcular_carga_admissivel(self) -> float:
        return self.capacidade_solo * self.calcular_area_base()

    def verificar_ruptura_solo(self) -> bool:
        return self.carga > self.calcular_carga_admissivel()

    def calcular_armacao_longitudinal(self) -> Dict[str, float]:
        armadura_minima = 0.0025
        area_aco = armadura_minima * math.pi * (self.diametro / 2) ** 2
        diametro_barras = 20 / 1000
        area_barra = (math.pi * diametro_barras ** 2) / 4
        quantidade_barras = area_aco / area_barra
        return {
            "quantidade_barras": quantidade_barras,
            "diametro_barras": diametro_barras * 1000,
        }

    def calcular_armacao_transversal(self) -> Dict[str, float]:
        armadura_minima = 0.0015
        area_aco_transversal = armadura_minima * self.diametro * self.profundidade
        diametro_estribos = 12 / 1000
        area_estribo = (math.pi * diametro_estribos ** 2) / 4
        quantidade_estribos = area_aco_transversal / area_estribo
        return {
            "quantidade_estribos": quantidade_estribos,
            "diametro_estribos": diametro_estribos * 1000,
        }

    def calcular_assentamento_solo(self) -> float:
        modulo_deformacao = 15000
        tensao_no_solo = self.calcular_tensao_no_solo()
        return (tensao_no_solo / modulo_deformacao) * self.profundidade * 1000

    def gerar_relatorio(self) -> Dict[str, float]:
        return {
            "Área da Base (m²)": self.calcular_area_base(),
            "Volume de Concreto (m³)": self.calcular_volume_concreto(),
            "Peso do Concreto (kN)": self.calcular_peso_concreto(),
            "Tensão no Solo (kN/m²)": self.calcular_tensao_no_solo(),
            "Carga Admissível (kN)": self.calcular_carga_admissivel(),
            "Ruptura do Solo": self.verificar_ruptura_solo(),
            "Armadura Longitudinal - Quantidade de Barras": self.calcular_armacao_longitudinal()["quantidade_barras"],
            "Armadura Longitudinal - Diâmetro das Barras (mm)": self.calcular_armacao_longitudinal()["diametro_barras"],
            "Armadura Transversal - Quantidade de Estribos": self.calcular_armacao_transversal()["quantidade_estribos"],
            "Armadura Transversal - Diâmetro dos Estribos (mm)": self.calcular_armacao_transversal()["diametro_estribos"],
            "Assentamento Estimado do Solo (mm)": self.calcular_assentamento_solo(),
        }
