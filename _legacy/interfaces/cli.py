import logging
import argparse
import sys
from src.lct_calculator.calculators import Sapata, Bloco, Tubulao, Estaca, Radier, Barrete, SapataCorrida, EstacaHeliceContinua, TubulaoCeuAberto, TubulaoArComprimido
from src.lct_calculator.database import DatabaseService
from src.lct_calculator.interfaces.report_generator import ReportGenerator

# Configurando o logger
logging.basicConfig(level=logging.INFO)

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
            'sapata', 'bloco', 'tubulão', 'estaca', 'radier',
            'barrete', 'sapata_corrida', 'estaca_helice_continua',
            'tubulão_céu_aberto', 'tubulão_sob_ar_comprimido'
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
        logging.info(f"Iniciando cálculo de {tipo} com área {area} m² e força {forca} kN.")
        try:
            # Mapeamento das classes para cada tipo de fundação
            fundacoes = {
                'sapata': Sapata,
                'bloco': Bloco,
                'tubulão': Tubulao,
                'estaca': Estaca,
                'radier': Radier,
                'barrete': Barrete,
                'sapata_corrida': SapataCorrida,
                'estaca_helice_continua': EstacaHeliceContinua,
                'tubulão_céu_aberto': TubulaoCeuAberto,
                'tubulão_sob_ar_comprimido': TubulaoArComprimido
            }

            # Seleciona a classe correta para o tipo de fundação
            classe_fundacao = fundacoes.get(tipo)
            if not classe_fundacao:
                raise ValueError(f"Tipo de fundação '{tipo}' não é suportado.")
            
            # Exemplo de parâmetros adicionais, ajustados conforme necessário para cada tipo
            if tipo == 'sapata':
                fundacao = classe_fundacao(carga=forca, fck=25, base=area**0.5, altura=1.0, capacidade_solo=150)
            elif tipo == 'tubulão':
                fundacao = classe_fundacao(carga=forca, fck=25, diametro=1.0, altura=3.0, tipo="Céu Aberto", escavacao_prof=5.0, profundidade_agua=1.5)
            else:
                fundacao = classe_fundacao(carga=forca, fck=25, diametro=1.0, altura=2.0, capacidade_solo=150)  # Ajuste conforme necessário

            resultado = fundacao.gerar_relatorio()

            # Salvar no banco de dados
            dados_entrada = f"Área: {area} m², Força: {forca} kN"
            self.db_service.salvar_calculo(tipo, dados_entrada, str(resultado))
            print(f"Resultado do cálculo de {tipo}: {resultado}")
        except Exception as e:
            print(f"Erro ao calcular a fundação: {e}")
            sys.exit(1)

    def gerar_relatorio(self, formato, caminho_arquivo):
        """Gera um relatório baseado nos cálculos realizados"""
        try:
            # Exemplo de dados que poderiam ser extraídos do banco de dados
            dados = self.db_service.buscar_calculos()
            relatorio = ReportGenerator(dados=dados, nome_projeto="Projeto Exemplo", engenheiro_responsavel="Eng. Rafael Dias")
            relatorio.gerar_relatorio(formato, caminho_arquivo)
            print(f"Relatório gerado com sucesso: {caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao gerar o relatório: {e}")
            sys.exit(1)

# Exemplo de uso da CLI
if __name__ == "__main__":
    cli = CLI()
    cli.executar()
