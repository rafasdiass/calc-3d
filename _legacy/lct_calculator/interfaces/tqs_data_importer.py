import os
import csv
import json
import ifcopenshell
from typing import List, Dict, Union
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

class TQSDataImporter:
    """
    Classe responsável por importar dados de arquivos do TQS (.csv, .json, .ifc).
    """

    @staticmethod
    def carregar_csv(caminho_arquivo: str) -> List[Dict[str, Union[str, float, int]]]:
        """
        Carrega dados de um arquivo CSV e retorna uma lista de dicionários.
        
        :param caminho_arquivo: Caminho do arquivo CSV.
        :return: Lista de dicionários contendo os dados do CSV.
        """
        if not os.path.exists(caminho_arquivo):
            logging.error(f"Arquivo CSV não encontrado: {caminho_arquivo}")
            raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado.")
        
        try:
            with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                dados = [linha for linha in reader]
            logging.info(f"Dados do arquivo CSV {caminho_arquivo} carregados com sucesso.")
            return dados
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo CSV: {e}")
            raise

    @staticmethod
    def carregar_json(caminho_arquivo: str) -> Union[Dict, List]:
        """
        Carrega dados de um arquivo JSON.
        
        :param caminho_arquivo: Caminho do arquivo JSON.
        :return: Dicionário ou lista com os dados JSON.
        """
        if not os.path.exists(caminho_arquivo):
            logging.error(f"Arquivo JSON não encontrado: {caminho_arquivo}")
            raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado.")
        
        try:
            with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
                dados = json.load(file)
            logging.info(f"Dados do arquivo JSON {caminho_arquivo} carregados com sucesso.")
            return dados
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar o arquivo JSON: {caminho_arquivo}")
            raise
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo JSON: {e}")
            raise

    @staticmethod
    def carregar_dados_ifc(caminho_arquivo: str) -> ifcopenshell.file:
        """
        Carrega dados de um arquivo IFC (integrado ao TQS).
        
        :param caminho_arquivo: Caminho do arquivo IFC.
        :return: Objeto ifcopenshell.file contendo os dados do arquivo IFC.
        """
        if not os.path.exists(caminho_arquivo):
            logging.error(f"Arquivo IFC não encontrado: {caminho_arquivo}")
            raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado.")
        
        try:
            model = ifcopenshell.open(caminho_arquivo)
            logging.info(f"Arquivo IFC {caminho_arquivo} carregado com sucesso.")
            return model
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo IFC: {e}")
            raise

    @staticmethod
    def extrair_informacoes_ifc(modelo_ifc: ifcopenshell.file) -> Dict[str, Union[str, float]]:
        """
        Extrai informações essenciais do arquivo IFC (exemplo: dimensões da fundação, materiais, etc.).
        
        :param modelo_ifc: Objeto ifcopenshell.file carregado.
        :return: Dicionário contendo as informações essenciais extraídas.
        """
        fundacoes = {}
        try:
            for fundacao in modelo_ifc.by_type("IfcFooting"):
                fundacoes[fundacao.GlobalId] = {
                    "Tipo": fundacao.ObjectType,
                    "Nome": fundacao.Name,
                    "Largura": fundacao.OverallWidth if hasattr(fundacao, 'OverallWidth') else 'N/A',
                    "Comprimento": fundacao.OverallLength if hasattr(fundacao, 'OverallLength') else 'N/A',
                }
            logging.info("Informações extraídas com sucesso do arquivo IFC.")
            return fundacoes
        except Exception as e:
            logging.error(f"Erro ao extrair informações do modelo IFC: {e}")
            raise


# Exemplo de uso
if __name__ == "__main__":
    import argparse

    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(description="Importador de Dados TQS")
    parser.add_argument('--file', type=str, required=True, help="Caminho do arquivo a ser importado (CSV, JSON ou IFC)")
    
    args = parser.parse_args()

    # Processando o arquivo
    try:
        extensao = os.path.splitext(args.file)[1].lower()
        if extensao == '.csv':
            dados = TQSDataImporter.carregar_csv(args.file)
            print("Dados carregados do CSV:", dados)
        elif extensao == '.json':
            dados = TQSDataImporter.carregar_json(args.file)
            print("Dados carregados do JSON:", dados)
        elif extensao == '.ifc':
            modelo_ifc = TQSDataImporter.carregar_dados_ifc(args.file)
            fundacoes = TQSDataImporter.extrair_informacoes_ifc(modelo_ifc)
            print("Fundação extraídas do IFC:", fundacoes)
        else:
            raise ValueError("Formato de arquivo não suportado.")
    except Exception as e:
        print(f"Erro: {e}")
