import math
from typing import Union

class SimpleCalculator:
    """
    Calculadora simples com suporte a operações matemáticas básicas e cálculos financeiros avançados, 
    como juros simples e compostos.
    """

    def __init__(self):
        pass

    # Operações matemáticas básicas
    def add(self, a: float, b: float) -> float:
        """Adiciona dois números."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtrai o segundo número do primeiro."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplica dois números."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide o primeiro número pelo segundo, com tratamento de divisão por zero."""
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Calcula a exponenciação de um número."""
        return math.pow(base, exponent)

    def sqrt(self, number: float) -> float:
        """Calcula a raiz quadrada de um número."""
        if number < 0:
            raise ValueError("Não é possível calcular a raiz quadrada de um número negativo.")
        return math.sqrt(number)

    # Cálculos financeiros
    def juros_simples(self, capital: float, taxa: float, tempo: float) -> float:
        """
        Calcula o montante com base no cálculo de juros simples.
        Fórmula: M = C * (1 + i * t)
        :param capital: Capital inicial (C)
        :param taxa: Taxa de juros (i) em percentual
        :param tempo: Tempo (t) em anos
        :return: Montante final (M)
        """
        montante = capital * (1 + (taxa / 100) * tempo)
        return montante

    def juros_compostos(self, capital: float, taxa: float, tempo: float) -> float:
        """
        Calcula o montante com base no cálculo de juros compostos.
        Fórmula: M = C * (1 + i)^t
        :param capital: Capital inicial (C)
        :param taxa: Taxa de juros (i) em percentual
        :param tempo: Tempo (t) em anos
        :return: Montante final (M)
        """
        montante = capital * math.pow((1 + taxa / 100), tempo)
        return montante

    def calcular_taxa_equivalente(self, taxa_efetiva: float, periodo: float) -> float:
        """
        Calcula a taxa equivalente para diferentes períodos de capitalização.
        Fórmula: i_eq = (1 + i_efetiva)^(1/n) - 1
        :param taxa_efetiva: Taxa efetiva anual
        :param periodo: Número de períodos em um ano
        :return: Taxa equivalente por período
        """
        taxa_equivalente = math.pow((1 + taxa_efetiva / 100), (1 / periodo)) - 1
        return taxa_equivalente * 100

    # Operações matemáticas avançadas
    def factorial(self, number: int) -> int:
        """Calcula o fatorial de um número inteiro."""
        if number < 0:
            raise ValueError("Não é possível calcular o fatorial de um número negativo.")
        return math.factorial(number)

    def logarithm(self, number: float, base: Union[int, float] = math.e) -> float:
        """
        Calcula o logaritmo de um número com a base especificada (por padrão, base natural e).
        :param number: O número de entrada
        :param base: A base do logaritmo (por padrão, e)
        :return: O logaritmo de number na base especificada
        """
        if number <= 0:
            raise ValueError("O número deve ser maior que zero para calcular o logaritmo.")
        return math.log(number, base)

    def compound_interest_rate(self, montante: float, capital: float, tempo: float) -> float:
        """
        Calcula a taxa de juros compostos com base no montante final, capital e tempo.
        Fórmula: i = (M / C)^(1/t) - 1
        :param montante: Montante final (M)
        :param capital: Capital inicial (C)
        :param tempo: Tempo (t) em anos
        :return: Taxa de juros (i) em percentual
        """
        if capital <= 0:
            raise ValueError("O capital deve ser maior que zero.")
        if montante <= capital:
            raise ValueError("O montante final deve ser maior que o capital.")
        return (math.pow(montante / capital, 1 / tempo) - 1) * 100

    def present_value(self, montante: float, taxa: float, tempo: float) -> float:
        """
        Calcula o valor presente com base em juros compostos.
        Fórmula: PV = M / (1 + i)^t
        :param montante: Montante final (M)
        :param taxa: Taxa de juros (i) em percentual
        :param tempo: Tempo (t) em anos
        :return: Valor presente (PV)
        """
        return montante / math.pow((1 + taxa / 100), tempo)

    def future_value(self, capital: float, taxa: float, tempo: float) -> float:
        """
        Calcula o valor futuro de um investimento com base em juros compostos.
        Fórmula: FV = PV * (1 + i)^t
        :param capital: Capital inicial (PV)
        :param taxa: Taxa de juros (i) em percentual
        :param tempo: Tempo (t) em anos
        :return: Valor futuro (FV)
        """
        return capital * math.pow((1 + taxa / 100), tempo)

    def discounted_cash_flow(self, fluxos_de_caixa: list, taxa_desconto: float) -> float:
        """
        Calcula o valor presente líquido (VPL) de uma série de fluxos de caixa usando desconto.
        :param fluxos_de_caixa: Lista de fluxos de caixa por período
        :param taxa_desconto: Taxa de desconto em percentual
        :return: Valor presente líquido (VPL)
        """
        vpl = sum(fluxo / math.pow((1 + taxa_desconto / 100), t) for t, fluxo in enumerate(fluxos_de_caixa, start=1))
        return vpl

# Exemplo de uso da SimpleCalculator
if __name__ == "__main__":
    calc = SimpleCalculator()

    # Operações básicas
    print(f"Soma: {calc.add(10, 5)}")
    print(f"Divisão: {calc.divide(100, 4)}")
    print(f"Exponenciação: {calc.power(2, 10)}")
    print(f"Fatorial: {calc.factorial(5)}")

    # Cálculos financeiros
    capital_inicial = 1000
    taxa_juros = 5  # 5%
    tempo_anos = 10

    montante_simples = calc.juros_simples(capital_inicial, taxa_juros, tempo_anos)
    montante_composto = calc.juros_compostos(capital_inicial, taxa_juros, tempo_anos)

    print(f"Montante com juros simples: {montante_simples}")
    print(f"Montante com juros compostos: {montante_composto}")

    # Valor presente e futuro
    valor_futuro = calc.future_value(capital_inicial, taxa_juros, tempo_anos)
    print(f"Valor futuro: {valor_futuro}")

    valor_presente = calc.present_value(valor_futuro, taxa_juros, tempo_anos)
    print(f"Valor presente: {valor_presente}")
