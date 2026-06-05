import argparse
import logging
import sys

from lct_calculator.calculators import (
    Sapata,
    Bloco,
    Tubulao,
    Estaca,
    Radier,
    Barrete,
    SapataCorrida,
    EstacaHeliceContinua,
    TubulaoCeuAberto,
    TubulaoArComprimido,
)
from lct_calculator.database import DatabaseService
from lct_calculator.interfaces.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class CLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Calculadora de Fundações CLI")
        self.db_service = DatabaseService()
        self.setup_commands()

    def setup_commands(self) -> None:
        """Configura os comandos disponíveis na CLI."""
        subparsers = self.parser.add_subparsers(dest="command")

        calcular_parser = subparsers.add_parser("calcular", help="Calcular fundação")
        calcular_parser.add_argument(
            "tipo",
            choices=[
                "sapata",
                "bloco",
                "tubulao",
                "estaca",
                "radier",
                "barrete",
                "sapata_corrida",
                "estaca_helice_continua",
                "tubulao_ceu_aberto",
                "tubulao_ar_comprimido",
            ],
            help="Tipo de fundação",
        )
        calcular_parser.add_argument(
            "--area", required=True, type=float, help="Área da fundação (m²)"
        )
        calcular_parser.add_argument(
            "--forca", required=True, type=float, help="Força aplicada na fundação (kN)"
        )

        gerar_relatorio_parser = subparsers.add_parser(
            "gerar-relatorio", help="Gerar relatório de fundações"
        )
        gerar_relatorio_parser.add_argument(
            "formato", choices=["csv", "json", "pdf"], help="Formato do relatório"
        )
        gerar_relatorio_parser.add_argument(
            "--file", required=True, type=str, help="Caminho para o arquivo de saída"
        )

    def executar(self, args: list[str] | None = None) -> None:
        """Executa os comandos com base nos argumentos da linha de comando."""
        parsed = self.parser.parse_args(args)

        if parsed.command == "calcular":
            self.calcular_fundacao(parsed.tipo, parsed.area, parsed.forca)
        elif parsed.command == "gerar-relatorio":
            self.gerar_relatorio(parsed.formato, parsed.file)

    def calcular_fundacao(self, tipo: str, area: float, forca: float) -> None:
        """Executa o cálculo da fundação e salva no banco de dados."""
        logger.info(
            "Iniciando cálculo de %s com área %.2f m² e força %.2f kN.", tipo, area, forca
        )
        try:
            fundacoes = {
                "sapata": Sapata,
                "bloco": Bloco,
                "tubulao": Tubulao,
                "estaca": Estaca,
                "radier": Radier,
                "barrete": Barrete,
                "sapata_corrida": SapataCorrida,
                "estaca_helice_continua": EstacaHeliceContinua,
                "tubulao_ceu_aberto": TubulaoCeuAberto,
                "tubulao_ar_comprimido": TubulaoArComprimido,
            }

            classe_fundacao = fundacoes.get(tipo)
            if not classe_fundacao:
                raise ValueError(f"Tipo de fundação '{tipo}' não é suportado.")

            if tipo == "sapata":
                fundacao = classe_fundacao(
                    carga=forca, fck=25, base=area**0.5, altura=1.0, capacidade_solo=150
                )
            elif tipo == "tubulao":
                fundacao = classe_fundacao(
                    carga=forca,
                    fck=25,
                    diametro=1.0,
                    altura=3.0,
                    tipo="Céu Aberto",
                    escavacao_prof=5.0,
                    profundidade_agua=1.5,
                )
            else:
                fundacao = classe_fundacao(
                    carga=forca, fck=25, diametro=1.0, altura=2.0, capacidade_solo=150
                )

            resultado = fundacao.gerar_relatorio()
            dados_entrada = f"Área: {area} m², Força: {forca} kN"
            self.db_service.salvar_calculo(tipo, dados_entrada, str(resultado))
            print(f"Resultado do cálculo de {tipo}: {resultado}")
        except Exception as exc:
            print(f"Erro ao calcular a fundação: {exc}")
            sys.exit(1)

    def gerar_relatorio(self, formato: str, caminho_arquivo: str) -> None:
        """Gera um relatório baseado nos cálculos realizados."""
        try:
            dados = self.db_service.buscar_calculos()
            relatorio = ReportGenerator(
                dados=dados,
                nome_projeto="Projeto Exemplo",
                engenheiro_responsavel="Eng. Rafael Dias",
            )
            relatorio.gerar_relatorio(formato, caminho_arquivo)
            print(f"Relatório gerado com sucesso: {caminho_arquivo}")
        except Exception as exc:
            print(f"Erro ao gerar o relatório: {exc}")
            sys.exit(1)


if __name__ == "__main__":
    cli = CLI()
    cli.executar()
