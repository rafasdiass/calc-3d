import argparse
import sys
from database.database_service import DatabaseService
from reports.report_generator import ReportGenerator
from calculations.calculators import Sapata, Bloco, Tubulao, Estaca, Radier, Barrete, SapataCorrida, EstacaHeliceContinua, TubulaoCeuAberto, TubulaoArComprimido
from config.logger_config import configure_logger

configure_logger()

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Calculadora de Fundações CLI")
        self.db_service = DatabaseService()
        self.setup_commands()

    def setup_commands(self):
        """Configura os comandos disponíveis na CLI"""
        subparsers = self.parser.add_subparsers(dest="command")

        # Comando para calcular fundações
        calcular_parser = subparsers.add_parser("calcular", help="Calcular fundação")
        calcular_parser.add_argument("tipo", choices=[
            'sapata', 'bloco', 'tubulão', 'estaca', 'radier', 'barrete',
            'sapata_corrida', 'estaca_helice_continua', 'tubulão_céu_aberto', 'tubulão_sob_ar_comprimido'
        ], help="Tipo de fundação")
        calcular_parser.add_argument("--area", required=True, type=float, help="Área da fundação (m²)")
        calcular_parser.add_argument("--forca", required=True, type=float, help="Força aplicada na fundação (kN)")

        # Comando para gerar relatório
        gerar_relatorio_parser = subparsers.add_parser("gerar-relatorio", help="Gerar relatório de fundações")
        gerar_relatorio_parser.add_argument("formato", choices=['csv', 'json', 'pdf'], help="Formato do relatório")
        gerar_relatorio_parser.add_argument("--file", required=True, type=str, help="Caminho para o arquivo de saída")

    def executar(self, args=None):
        """Executa os comandos com base nos argumentos da linha de comando"""
        args = self.parser.parse_args(args)
        if args.command == "calcular":
            self.calcular_fundacao(args.tipo, args.area, args.forca)
        elif args.command == "gerar-relatorio":
            self.gerar_relatorio(args.formato, args.file)

    def calcular_fundacao(self, tipo, area, forca):
        """Executa o cálculo da fundação e salva no banco de dados"""
        fundacoes = {
            'sapata': Sapata, 'bloco': Bloco, 'tubulão': Tubulao, 'estaca': Estaca,
            'radier': Radier, 'barrete': Barrete, 'sapata_corrida': SapataCorrida,
            'estaca_helice_continua': EstacaHeliceContinua, 'tubulão_céu_aberto': TubulaoCeuAberto,
            'tubulão_sob_ar_comprimido': TubulaoArComprimido
        }
        classe_fundacao = fundacoes.get(tipo)
        if classe_fundacao:
            fundacao = classe_fundacao(carga=forca, fck=25, base=area**0.5, altura=1.0, capacidade_solo=150)
            resultado = fundacao.gerar_relatorio()
            dados_entrada = f"Área: {area} m², Força: {forca} kN"
            self.db_service.salvar_calculo(tipo, dados_entrada, str(resultado))
            print(f"Resultado do cálculo de {tipo}: {resultado}")

    def gerar_relatorio(self, formato, caminho_arquivo):
        """Gera um relatório baseado nos cálculos realizados"""
        dados = self.db_service.buscar_calculos()
        relatorio = ReportGenerator(dados=dados, nome_projeto="Projeto Exemplo", engenheiro_responsavel="Eng. Rafael Dias")
        relatorio.gerar_relatorio(formato, caminho_arquivo)

if __name__ == "__main__":
    cli = CLI()
    cli.executar()
