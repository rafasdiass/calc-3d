import os
import json
import csv
import logging
from typing import Dict, List, Any, Union

# Configuração do logger
logging.basicConfig(level=logging.INFO)

class FileHelper:
    """
    Classe auxiliar para manipulação de arquivos, incluindo leitura, escrita e validação de dados.
    Suporta arquivos JSON, CSV e formatos personalizados.
    """

    @staticmethod
    def carregar_arquivo(filepath: str) -> Union[Dict, List, None]:
        """
        Carrega um arquivo e retorna seus dados em formato apropriado (lista ou dicionário).
        Suporta JSON e CSV.
        
        :param filepath: Caminho para o arquivo a ser carregado.
        :return: Dados do arquivo em formato de lista ou dicionário.
        """
        if not os.path.exists(filepath):
            logging.error(f"Arquivo {filepath} não encontrado.")
            raise FileNotFoundError(f"Arquivo {filepath} não encontrado.")
        
        extensao = os.path.splitext(filepath)[1].lower()

        try:
            if extensao == ".json":
                return FileHelper._carregar_json(filepath)
            elif extensao == ".csv":
                return FileHelper._carregar_csv(filepath)
            else:
                logging.error(f"Formato de arquivo {extensao} não suportado.")
                raise ValueError(f"Formato de arquivo {extensao} não suportado.")
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def salvar_arquivo(filepath: str, dados: Union[Dict, List], formato: str = "json") -> None:
        """
        Salva os dados fornecidos em um arquivo. Suporta JSON e CSV.
        
        :param filepath: Caminho onde o arquivo será salvo.
        :param dados: Dados a serem salvos (dicionário ou lista).
        :param formato: Formato de saída ('json' ou 'csv').
        """
        if formato not in ["json", "csv"]:
            logging.error(f"Formato {formato} não suportado para exportação.")
            raise ValueError(f"Formato {formato} não suportado para exportação.")

        try:
            if formato == "json":
                FileHelper._salvar_json(filepath, dados)
            elif formato == "csv":
                FileHelper._salvar_csv(filepath, dados)
            logging.info(f"Arquivo salvo com sucesso em {filepath}")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def _carregar_json(filepath: str) -> Dict:
        """Carrega um arquivo JSON e retorna os dados como um dicionário."""
        try:
            with open(filepath, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON no arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def _salvar_json(filepath: str, dados: Dict) -> None:
        """Salva dados em formato JSON no arquivo especificado."""
        try:
            with open(filepath, 'w', encoding='utf-8') as json_file:
                json.dump(dados, json_file, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"Erro de I/O ao salvar JSON no arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def _carregar_csv(filepath: str) -> List[Dict[str, Any]]:
        """Carrega um arquivo CSV e retorna os dados como uma lista de dicionários."""
        try:
            with open(filepath, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                return [row for row in reader]
        except csv.Error as e:
            logging.error(f"Erro ao ler CSV no arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def _salvar_csv(filepath: str, dados: List[Dict[str, Any]]) -> None:
        """Salva dados em formato CSV no arquivo especificado."""
        if not isinstance(dados, list) or not all(isinstance(row, dict) for row in dados):
            logging.error("Dados fornecidos para CSV não estão no formato correto.")
            raise ValueError("Dados fornecidos para CSV devem ser uma lista de dicionários.")

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=dados[0].keys())
                writer.writeheader()
                writer.writerows(dados)
        except IOError as e:
            logging.error(f"Erro de I/O ao salvar CSV no arquivo {filepath}: {str(e)}")
            raise

    @staticmethod
    def validar_caminho(filepath: str) -> bool:
        """
        Valida se o caminho do arquivo é válido.
        
        :param filepath: Caminho para o arquivo.
        :return: True se o arquivo existir e for acessível, False caso contrário.
        """
        if os.path.exists(filepath) and os.access(filepath, os.R_OK):
            logging.info(f"O arquivo {filepath} é válido e acessível.")
            return True
        else:
            logging.error(f"Arquivo {filepath} inválido ou inacessível.")
            return False

    @staticmethod
    def listar_arquivos_diretorio(diretorio: str, extensao: str = "*") -> List[str]:
        """
        Lista arquivos em um diretório com uma extensão específica.
        
        :param diretorio: Caminho para o diretório.
        :param extensao: Extensão de arquivos a serem listados (ex: ".json", ".csv"). Usa "*" para listar todos os arquivos.
        :return: Lista de caminhos de arquivos.
        """
        if not os.path.isdir(diretorio):
            logging.error(f"O caminho {diretorio} não é um diretório válido.")
            raise NotADirectoryError(f"O caminho {diretorio} não é um diretório válido.")

        arquivos = [os.path.join(diretorio, f) for f in os.listdir(diretorio) if f.endswith(extensao) or extensao == "*"]
        logging.info(f"Arquivos encontrados no diretório {diretorio}: {arquivos}")
        return arquivos

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de carregamento de arquivo
    try:
        dados = FileHelper.carregar_arquivo("dados_exemplo.json")
        print(dados)

        # Exemplo de salvamento de arquivo
        FileHelper.salvar_arquivo("relatorio_exemplo.csv", dados, formato="csv")
    except Exception as e:
        logging.error(f"Erro durante a execução do exemplo: {e}")
