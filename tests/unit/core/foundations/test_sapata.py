"""
Testes unitários para Sapata (core/foundations/sapata.py).

Cobertura: área, volume, tensão solo, carga admissível, ruptura, armação, relatório.
Não requer banco de dados, HTTP ou qualquer I/O externo.
"""
import math
import pytest

from lct_calculator.core.foundations.sapata import Sapata


@pytest.fixture
def sapata_padrao() -> Sapata:
    """
    Sapata com valores determinísticos para todos os asserts.
    base=2.0m, altura=0.5m, carga=500kN, fck=25MPa, capacidade_solo=200kN/m²
    """
    return Sapata(
        carga=500.0,
        fck=25.0,
        base=2.0,
        altura=0.5,
        capacidade_solo=200.0,
    )


@pytest.fixture
def sapata_ruptura() -> Sapata:
    """Sapata onde carga (2000kN) > carga admissível (200 * 4 = 800kN)."""
    return Sapata(
        carga=2000.0,
        fck=25.0,
        base=2.0,
        altura=0.5,
        capacidade_solo=200.0,
    )


class TestSapataArea:
    def test_area_base_quadrada(self, sapata_padrao: Sapata) -> None:
        """Área = base² = 2.0² = 4.0 m²."""
        assert sapata_padrao.calcular_area() == pytest.approx(4.0)

    def test_area_base_unitaria(self) -> None:
        s = Sapata(carga=100.0, fck=20.0, base=1.0, altura=0.3, capacidade_solo=150.0)
        assert s.calcular_area() == pytest.approx(1.0)


class TestSapataVolume:
    def test_volume_concreto(self, sapata_padrao: Sapata) -> None:
        """Volume = base² * altura = 4.0 * 0.5 = 2.0 m³."""
        assert sapata_padrao.calcular_volume_concreto() == pytest.approx(2.0)

    def test_peso_concreto_padrao(self, sapata_padrao: Sapata) -> None:
        """Peso = volume * 25 kN/m³ = 2.0 * 25 = 50 kN."""
        assert sapata_padrao.calcular_peso_concreto() == pytest.approx(50.0)

    def test_peso_concreto_custom(self) -> None:
        s = Sapata(carga=100.0, fck=20.0, base=1.0, altura=1.0, capacidade_solo=150.0, peso_concreto=24.0)
        assert s.calcular_peso_concreto() == pytest.approx(24.0)


class TestSapataTensaoSolo:
    def test_tensao_no_solo(self, sapata_padrao: Sapata) -> None:
        """Tensão = carga / área = 500 / 4 = 125 kN/m²."""
        assert sapata_padrao.calcular_tensao_no_solo() == pytest.approx(125.0)


class TestSapataCargaAdmissivel:
    def test_carga_admissivel(self, sapata_padrao: Sapata) -> None:
        """Carga adm = capacidade_solo * área = 200 * 4 = 800 kN."""
        assert sapata_padrao.calcular_carga_admissivel() == pytest.approx(800.0)


class TestSapataRuptura:
    def test_sem_ruptura(self, sapata_padrao: Sapata) -> None:
        """500 kN < 800 kN → sem ruptura."""
        assert sapata_padrao.verificar_ruptura_solo() is False

    def test_com_ruptura(self, sapata_ruptura: Sapata) -> None:
        """2000 kN > 800 kN → ruptura."""
        assert sapata_ruptura.verificar_ruptura_solo() is True


class TestSapataArmacao:
    def test_armacao_retorna_chaves_corretas(self, sapata_padrao: Sapata) -> None:
        resultado = sapata_padrao.calcular_armacao()
        assert "quantidade_barras" in resultado
        assert "diametro_barras" in resultado

    def test_armacao_diametro_mm(self, sapata_padrao: Sapata) -> None:
        """Diâmetro deve ser 12 mm conforme implementação."""
        assert sapata_padrao.calcular_armacao()["diametro_barras"] == pytest.approx(12.0)

    def test_armacao_quantidade_positiva(self, sapata_padrao: Sapata) -> None:
        assert sapata_padrao.calcular_armacao()["quantidade_barras"] > 0


class TestSapataRelatorio:
    def test_relatorio_contem_todas_chaves(self, sapata_padrao: Sapata) -> None:
        relatorio = sapata_padrao.gerar_relatorio()
        chaves_esperadas = {
            "Área da Base (m²)",
            "Tensão no Solo (kN/m²)",
            "Volume de Concreto (m³)",
            "Peso do Concreto (kN)",
            "Carga Admissível (kN)",
            "Ruptura do Solo",
            "Armadura - Quantidade de Barras",
            "Armadura - Diâmetro das Barras (mm)",
        }
        assert chaves_esperadas == set(relatorio.keys())

    def test_relatorio_valores_consistentes(self, sapata_padrao: Sapata) -> None:
        relatorio = sapata_padrao.gerar_relatorio()
        assert relatorio["Área da Base (m²)"] == pytest.approx(sapata_padrao.calcular_area())
        assert relatorio["Carga Admissível (kN)"] == pytest.approx(sapata_padrao.calcular_carga_admissivel())
        assert relatorio["Ruptura do Solo"] is False
