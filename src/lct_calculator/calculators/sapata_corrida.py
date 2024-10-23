import math
from typing import Dict, Tuple


class SapataCorrida:
    """Classe responsável pelo cálculo de uma Sapata Corrida."""

    def __init__(self, largura_base: float, altura_sapata: float, comprimento_sapata: float, fck: float, carga_kN: float,
                 cobrimento: float, diametro_aco: float, angulo_atrito_solo: float, peso_proprio_solo: float):
        """
        Inicializa os parâmetros da Sapata Corrida.

        :param largura_base: Largura da base da sapata em metros
        :param altura_sapata: Altura total da sapata em metros
        :param comprimento_sapata: Comprimento da sapata em metros
        :param fck: Resistência característica do concreto (em MPa)
        :param carga_kN: Carga aplicada sobre a sapata em kN
        :param cobrimento: Cobrimento nominal da armadura (em mm)
        :param diametro_aco: Diâmetro da armadura longitudinal (em mm)
        :param angulo_atrito_solo: Ângulo de atrito do solo (em graus)
        :param peso_proprio_solo: Peso específico do solo de fundação (em kN/m³)
        """
        self.largura_base = largura_base
        self.altura_sapata = altura_sapata
        self.comprimento_sapata = comprimento_sapata
        self.fck = fck
        self.carga_kN = carga_kN
        self.cobrimento = cobrimento / 1000  # Converte de mm para metros
        self.diametro_aco = diametro_aco / 1000  # Converte de mm para metros
        self.angulo_atrito_solo = math.radians(angulo_atrito_solo)  # Converte de graus para radianos
        self.peso_proprio_solo = peso_proprio_solo

    def calcular_tensao_solo(self) -> float:
        """Calcula a tensão admissível no solo devido à carga."""
        area_base = self.largura_base * self.comprimento_sapata
        tensao_solo = self.carga_kN / area_base
        return tensao_solo

    def calcular_armadura_flexao(self) -> Tuple[float, int]:
        """
        Calcula a armadura de flexão para a sapata corrida com base no momento máximo.

        :return: Área de aço necessária (em cm²) e o número de barras de aço
        """
        # Considerações de flexão (simulação de carregamento)
        momento_fletor_max = (self.carga_kN * self.largura_base) / 8  # Fórmula aproximada
        d = self.altura_sapata - self.cobrimento  # Altura útil da sapata
        momento_admissivel = 0.251 * self.fck * (d ** 2)

        if momento_fletor_max > momento_admissivel:
            raise ValueError("A sapata é insuficiente para resistir ao momento fletor calculado.")

        # Cálculo da área de aço necessária (utilizando a fórmula do momento resistente)
        area_aco_necessaria = momento_fletor_max / (0.87 * 500 * d)  # Tensão do aço assumida como 500 MPa
        numero_barras = math.ceil((area_aco_necessaria * 10000) / (math.pi * (self.diametro_aco ** 2) / 4))

        return area_aco_necessaria * 10000, numero_barras  # Convertendo área para cm²

    def calcular_cisalhamento(self) -> float:
        """
        Calcula a tensão de cisalhamento na sapata, verificando a resistência do concreto.

        :return: Tensão de cisalhamento (em MPa)
        """
        area_cisalhamento = self.largura_base * self.altura_sapata
        tensao_cisalhamento = self.carga_kN / area_cisalhamento
        resistencia_corte_concreto = 0.6 * math.sqrt(self.fck)

        if tensao_cisalhamento > resistencia_corte_concreto:
            raise ValueError("A sapata falha por cisalhamento.")

        return tensao_cisalhamento

    def verificar_estabilidade(self) -> bool:
        """Verifica a estabilidade ao deslizamento da sapata corrida."""
        forca_normal_solo = self.carga_kN - (self.peso_proprio_solo * self.largura_base * self.altura_sapata)
        resistencia_deslizamento = forca_normal_solo * math.tan(self.angulo_atrito_solo)

        if resistencia_deslizamento < self.carga_kN:
            raise ValueError("A sapata não é estável ao deslizamento.")
        
        return True

    def calcular_volume_concreto(self) -> float:
        """Calcula o volume de concreto necessário para a sapata."""
        volume = self.largura_base * self.comprimento_sapata * self.altura_sapata
        return volume

    def calcular(self) -> Dict[str, float]:
        """Executa todos os cálculos da sapata corrida e retorna os resultados em um dicionário."""
        resultados = {
            "Tensão no solo (kN/m²)": self.calcular_tensao_solo(),
            "Área de aço necessária (cm²)": self.calcular_armadura_flexao()[0],
            "Número de barras de aço": self.calcular_armadura_flexao()[1],
            "Tensão de cisalhamento (MPa)": self.calcular_cisalhamento(),
            "Volume de concreto (m³)": self.calcular_volume_concreto(),
            "Estabilidade ao deslizamento": self.verificar_estabilidade(),
        }

        return resultados


# Exemplo de uso (com parâmetros realistas)
if __name__ == "__main__":
    sapata_corrida = SapataCorrida(
        largura_base=1.2,
        altura_sapata=0.5,
        comprimento_sapata=3.0,
        fck=25,  # MPa
        carga_kN=500,
        cobrimento=30,  # mm
        diametro_aco=20,  # mm
        angulo_atrito_solo=30,  # graus
        peso_proprio_solo=18  # kN/m³
    )

    resultados = sapata_corrida.calcular()
    for chave, valor in resultados.items():
        print(f"{chave}: {valor}")
