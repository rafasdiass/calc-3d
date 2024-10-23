import csv
import json
from fpdf import FPDF
from typing import List, Dict, Union
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

class ReportGenerator:
    """
    Classe para geração de relatórios com base em dados de cálculo de fundações.
    Suporta múltiplos formatos: CSV, JSON e PDF.
    """

    def __init__(self, dados: List[Dict[str, Union[str, float, int]]], nome_projeto: str, engenheiro_responsavel: str):
        """
        Inicializa o gerador de relatórios com os dados necessários.
        :param dados: Lista de dicionários contendo os dados calculados das fundações.
        :param nome_projeto: Nome do projeto.
        :param engenheiro_responsavel: Nome do engenheiro responsável pelo projeto.
        """
        self.dados = dados
        self.nome_projeto = nome_projeto
        self.engenheiro_responsavel = engenheiro_responsavel

    def gerar_csv(self, caminho_arquivo: str):
        """
        Gera um relatório em formato CSV.
        :param caminho_arquivo: Caminho onde o arquivo CSV será salvo.
        """
        try:
            with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.dados[0].keys())
                writer.writeheader()
                writer.writerows(self.dados)
            logging.info(f"Relatório CSV gerado com sucesso: {caminho_arquivo}")
        except Exception as e:
            logging.error(f"Erro ao gerar relatório CSV: {e}")
            raise

    def gerar_json(self, caminho_arquivo: str):
        """
        Gera um relatório em formato JSON.
        :param caminho_arquivo: Caminho onde o arquivo JSON será salvo.
        """
        try:
            with open(caminho_arquivo, mode='w', encoding='utf-8') as file:
                json.dump({
                    "nome_projeto": self.nome_projeto,
                    "engenheiro_responsavel": self.engenheiro_responsavel,
                    "dados": self.dados
                }, file, indent=4)
            logging.info(f"Relatório JSON gerado com sucesso: {caminho_arquivo}")
        except Exception as e:
            logging.error(f"Erro ao gerar relatório JSON: {e}")
            raise

    def gerar_pdf(self, caminho_arquivo: str):
        """
        Gera um relatório em formato PDF.
        :param caminho_arquivo: Caminho onde o arquivo PDF será salvo.
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Cabeçalho
            pdf.cell(200, 10, txt=f"Relatório do Projeto: {self.nome_projeto}", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Engenheiro Responsável: {self.engenheiro_responsavel}", ln=True, align='C')

            # Adiciona uma linha em branco
            pdf.ln(10)

            # Adiciona os dados de cada fundação
            for fundacao in self.dados:
                for key, value in fundacao.items():
                    pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
                pdf.ln(5)

            # Salva o PDF no caminho especificado
            pdf.output(caminho_arquivo)
            logging.info(f"Relatório PDF gerado com sucesso: {caminho_arquivo}")
        except Exception as e:
            logging.error(f"Erro ao gerar relatório PDF: {e}")
            raise

    def gerar_relatorio(self, formato: str, caminho_arquivo: str):
        """
        Gera o relatório no formato especificado (CSV, JSON, PDF).
        :param formato: O formato desejado (csv, json, pdf).
        :param caminho_arquivo: Caminho onde o relatório será salvo.
        """
        if formato == 'csv':
            self.gerar_csv(caminho_arquivo)
        elif formato == 'json':
            self.gerar_json(caminho_arquivo)
        elif formato == 'pdf':
            self.gerar_pdf(caminho_arquivo)
        else:
            logging.error(f"Formato de relatório não suportado: {formato}")
            raise ValueError("Formato de relatório não suportado.")

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    dados_fundacoes = [
        {"Fundação": "Sapata", "Capacidade de Carga": 1500, "Volume de Concreto": 12.5},
        {"Fundação": "Estaca", "Capacidade de Carga": 2000, "Volume de Concreto": 10.0},
    ]

    nome_projeto = "Edifício Central"
    engenheiro_responsavel = "Eng. Rafael Dias"

    # Criando o gerador de relatórios
    gerador = ReportGenerator(dados=dados_fundacoes, nome_projeto=nome_projeto, engenheiro_responsavel=engenheiro_responsavel)

    # Gerando os relatórios nos formatos CSV, JSON e PDF
    gerador.gerar_relatorio('csv', 'relatorio_fundacoes.csv')
    gerador.gerar_relatorio('json', 'relatorio_fundacoes.json')
    gerador.gerar_relatorio('pdf', 'relatorio_fundacoes.pdf')
