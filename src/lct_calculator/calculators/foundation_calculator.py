from abc import ABC, abstractmethod
import math

class FoundationCalculation(ABC):
    """
    Classe base abstrata para cálculos gerais de fundações.
    Inclui cálculos de capacidade de carga, cisalhamento e dimensionamento de armaduras.
    """

    def __init__(self, fck: float, fyk: float, tensao_admissivel_solo: float):
        """
        Inicializa os parâmetros gerais da fundação.
        :param fck: Resistência característica do concreto (em MPa)
        :param fyk: Resistência característica do aço (em MPa)
        :param tensao_admissivel_solo: Tensão admissível do solo (em kN/m²)
        """
        if fck <= 0 or fyk <= 0 or tensao_admissivel_solo <= 0:
            raise ValueError("Todos os parâmetros devem ser maiores que zero.")
        self.fck = fck
        self.fyk = fyk
        self.tensao_admissivel_solo = tensao_admissivel_solo

    @abstractmethod
    def calcular_capacidade_carga(self) -> float:
        """Calcula a capacidade de carga da fundação (deve ser implementado por cada tipo específico de fundação)."""
        pass

    def calcular_volume_concreto(self, area_base: float, altura: float) -> float:
        """Calcula o volume de concreto para a fundação."""
        if area_base <= 0 or altura <= 0:
            raise ValueError("Área da base e altura devem ser maiores que zero.")
        return area_base * altura

    def calcular_armadura(self, momento_fletor: float, altura_util: float) -> float:
        """Calcula a área de aço necessária para a armadura."""
        if momento_fletor <= 0 or altura_util <= 0:
            raise ValueError("Momento fletor e altura útil devem ser maiores que zero.")
        momento_admissivel = 0.251 * self.fck * (altura_util ** 2)
        if momento_fletor > momento_admissivel:
            raise ValueError("Momento fletor excede o admissível.")
        area_aco_necessaria = momento_fletor / (0.87 * self.fyk * altura_util)
        return area_aco_necessaria * 10000  # Convertendo para cm²

    def calcular_resistencia_cisalhamento(self, carga: float, area_corte: float) -> float:
        """Calcula a tensão de cisalhamento e verifica se a fundação resiste ao corte."""
        if carga <= 0 or area_corte <= 0:
            raise ValueError("Carga e área de corte devem ser maiores que zero.")
        tensao_cisalhamento = carga / area_corte
        resistencia_cisalhamento = 0.6 * math.sqrt(self.fck)
        if tensao_cisalhamento > resistencia_cisalhamento:
            raise ValueError("Resistência ao cisalhamento é insuficiente.")
        return tensao_cisalhamento


class Sapata(FoundationCalculation):
    """Cálculo de uma sapata."""

    def __init__(self, largura: float, comprimento: float, altura: float, **kwargs):
        super().__init__(**kwargs)
        if largura <= 0 or comprimento <= 0 or altura <= 0:
            raise ValueError("Dimensões da sapata devem ser maiores que zero.")
        self.largura = largura
        self.comprimento = comprimento
        self.altura = altura

    def calcular_capacidade_carga(self) -> float:
        """Calcula a capacidade de carga específica para uma sapata."""
        area_base = self.largura * self.comprimento
        capacidade_carga = area_base * self.tensao_admissivel_solo
        return capacidade_carga

    def calcular_volume(self) -> float:
        """Calcula o volume de concreto necessário para a sapata."""
        return self.calcular_volume_concreto(self.largura * self.comprimento, self.altura)


class Estaca(FoundationCalculation):
    """Cálculo de uma estaca."""

    def __init__(self, diametro: float, profundidade: float, **kwargs):
        super().__init__(**kwargs)
        if diametro <= 0 or profundidade <= 0:
            raise ValueError("Dimensões da estaca devem ser maiores que zero.")
        self.diametro = diametro
        self.profundidade = profundidade

    def calcular_capacidade_carga(self) -> float:
        """Calcula a capacidade de carga específica para uma estaca."""
        area_base = math.pi * (self.diametro / 2) ** 2
        resistencia_ponta = area_base * self.tensao_admissivel_solo
        resistencia_lateral = math.pi * self.diametro * self.profundidade * self.tensao_admissivel_solo * 0.5
        return resistencia_ponta + resistencia_lateral

    def calcular_volume(self) -> float:
        """Calcula o volume de concreto necessário para a estaca."""
        area_base = math.pi * (self.diametro / 2) ** 2
        return self.calcular_volume_concreto(area_base, self.profundidade)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo para uma sapata
    sapata = Sapata(largura=2.0, comprimento=2.0, altura=0.5, fck=25, fyk=500, tensao_admissivel_solo=150)
    print(f"Capacidade de carga da sapata: {sapata.calcular_capacidade_carga()} kN")
    print(f"Volume de concreto da sapata: {sapata.calcular_volume()} m³")

    # Exemplo para uma estaca
    estaca = Estaca(diametro=0.6, profundidade=12, fck=30, fyk=500, tensao_admissivel_solo=100)
    print(f"Capacidade de carga da estaca: {estaca.calcular_capacidade_carga()} kN")
    print(f"Volume de concreto da estaca: {estaca.calcular_volume()} m³")
