import math
from typing import Dict, Tuple


class EstacaHeliceContinua:
    """Classe responsável pelo cálculo de uma Estaca Hélice Contínua."""

    def __init__(self, diametro_estaca: float, profundidade_estaca: float, fck: float, fyk: float,
                 carga_vertical_kN: float, tensao_admissivel_solo: float, cobrimento: float,
                 diametro_aco: float, peso_concreto: float):
        """
        Inicializa os parâmetros da Estaca Hélice Contínua.

        :param diametro_estaca: Diâmetro da estaca em metros
        :param profundidade_estaca: Profundidade da estaca em metros
        :param fck: Resistência característica do concreto (em MPa)
        :param fyk: Resistência característica do aço (em MPa)
        :param carga_vertical_kN: Carga vertical aplicada na estaca (em kN)
        :param tensao_admissivel_solo: Tensão admissível do solo (em kN/m²)
        :param cobrimento: Cobrimento nominal da armadura (em mm)
        :param diametro_aco: Diâmetro da armadura longitudinal (em mm)
        :param peso_concreto: Peso específico do concreto em kN/m³
        """
        self.diametro_estaca = diametro_estaca
        self.profundidade_estaca = profundidade_estaca
        self.fck = fck
        self.fyk = fyk
        self.carga_vertical_kN = carga_vertical_kN
        self.tensao_admissivel_solo = tensao_admissivel_solo
        self.cobrimento = cobrimento / 1000  # Converte de mm para metros
        self.diametro_aco = diametro_aco / 1000  # Converte de mm para metros
        self.peso_concreto = peso_concreto

    def calcular_area_base(self) -> float:
        """Calcula a área da base da estaca."""
        area_base = math.pi * (self.diametro_estaca / 2) ** 2
        return area_base

    def calcular_capacidade_carga(self) -> float:
        """
        Calcula a capacidade de carga da estaca considerando a resistência de ponta e lateral.

        :return: Capacidade de carga total da estaca em kN
        """
        area_base = self.calcular_area_base()
        resistencia_ponta = area_base * self.tensao_admissivel_solo  # Resistência de ponta
        resistencia_lateral = math.pi * self.diametro_estaca * self.profundidade_estaca * self.tensao_admissivel_solo * 0.5
        capacidade_total = resistencia_ponta + resistencia_lateral

        if capacidade_total < self.carga_vertical_kN:
            raise ValueError("A capacidade de carga da estaca é insuficiente.")

        return capacidade_total

    def calcular_armadura_flexao(self) -> Tuple[float, int]:
        """
        Calcula a área de aço necessária para resistir ao momento fletor.

        :return: Área de aço necessária (em cm²) e o número de barras de aço
        """
        momento_fletor_max = (self.carga_vertical_kN * self.diametro_estaca) / 8
        d = self.diametro_estaca - 2 * self.cobrimento
        momento_admissivel = 0.251 * self.fck * (d ** 2)

        if momento_fletor_max > momento_admissivel:
            raise ValueError("A estaca é insuficiente para resistir ao momento fletor calculado.")

        area_aco_necessaria = momento_fletor_max / (0.87 * self.fyk * d)
        numero_barras = math.ceil((area_aco_necessaria * 10000) / (math.pi * (self.diametro_aco ** 2) / 4))

        return area_aco_necessaria * 10000, numero_barras  # Convertendo área para cm²

    def calcular_resistencia_cisalhamento(self) -> float:
        """
        Calcula a tensão de cisalhamento na estaca, verificando a resistência ao cisalhamento do concreto.

        :return: Tensão de cisalhamento (em MPa)
        """
        area_cisalhamento = math.pi * self.diametro_estaca * self.profundidade_estaca
        tensao_cisalhamento = self.carga_vertical_kN / area_cisalhamento
        resistencia_corte_concreto = 0.6 * math.sqrt(self.fck)

        if tensao_cisalhamento > resistencia_corte_concreto:
            raise ValueError("A estaca falha por cisalhamento.")

        return tensao_cisalhamento

    def calcular_volume_concreto(self) -> float:
        """Calcula o volume de concreto necessário para a estaca."""
        volume_concreto = self.calcular_area_base() * self.profundidade_estaca
        return volume_concreto

    def verificar_estabilidade_arrancamento(self) -> bool:
        """
        Verifica a estabilidade da estaca ao arrancamento, considerando o peso próprio da estaca e o atrito lateral.

        :return: True se a estaca for estável ao arrancamento, caso contrário, False
        """
        peso_proprio_estaca = self.calcular_volume_concreto() * self.peso_concreto
        resistencia_atrito_lateral = math.pi * self.diametro_estaca * self.profundidade_estaca * self.tensao_admissivel_solo * 0.5
        resistencia_total_arrancamento = peso_proprio_estaca + resistencia_atrito_lateral

        if resistencia_total_arrancamento < self.carga_vertical_kN:
            raise ValueError("A estaca falha no critério de estabilidade ao arrancamento.")

        return True

    def calcular(self) -> Dict[str, float]:
        """Executa todos os cálculos da estaca hélice contínua e retorna os resultados em um dicionário."""
        resultados = {
            "Capacidade de carga (kN)": self.calcular_capacidade_carga(),
            "Área de aço necessária (cm²)": self.calcular_armadura_flexao()[0],
            "Número de barras de aço": self.calcular_armadura_flexao()[1],
            "Tensão de cisalhamento (MPa)": self.calcular_resistencia_cisalhamento(),
            "Volume de concreto (m³)": self.calcular_volume_concreto(),
            "Estabilidade ao arrancamento": self.verificar_estabilidade_arrancamento(),
        }

        return resultados


# Exemplo de uso (com parâmetros realistas)
if __name__ == "__main__":
    estaca_helice = EstacaHeliceContinua(
        diametro_estaca=0.6,
        profundidade_estaca=15.0,
        fck=30,  # MPa
        fyk=500,  # MPa (Aço CA-50)
        carga_vertical_kN=1200,
        tensao_admissivel_solo=150,  # kN/m²
        cobrimento=50,  # mm
        diametro_aco=25,  # mm
        peso_concreto=24  # kN/m³
    )

    resultados = estaca_helice.calcular()
    for chave, valor in resultados.items():
        print(f"{chave}: {valor}")
