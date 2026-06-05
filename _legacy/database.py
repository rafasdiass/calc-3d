import sqlite3
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(level=logging.INFO)

# Definindo o caminho do banco de dados
DATABASE_PATH = Path(__file__).parent / "lct_calculator.db"

class DatabaseService:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.create_tables()

    def connect(self):
        """Estabelece conexão com o banco de dados SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logging.info("Conexão com o banco de dados SQLite estabelecida.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def create_tables(self):
        """Cria as tabelas necessárias para armazenar os resultados dos cálculos"""
        self.connect()
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS fundacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    dados_entrada TEXT NOT NULL,
                    resultado TEXT NOT NULL,
                    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS relatorios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fundacao_id INTEGER,
                    caminho_arquivo TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(fundacao_id) REFERENCES fundacoes(id)
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sincronizacao_bim (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fundacao_id INTEGER,
                    status TEXT NOT NULL,
                    sincronizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(fundacao_id) REFERENCES fundacoes(id)
                );
            """)
            self.conn.commit()
            logging.info("Tabelas criadas com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar tabela: {e}")
            raise
        finally:
            self.close()

    def salvar_calculo(self, tipo, dados_entrada, resultado):
        """Insere um novo cálculo de fundação no banco de dados"""
        self.connect()
        try:
            self.cursor.execute("""
                INSERT INTO fundacoes (tipo, dados_entrada, resultado) 
                VALUES (?, ?, ?)
            """, (tipo, dados_entrada, resultado))
            self.conn.commit()
            logging.info(f"Cálculo de {tipo} salvo com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao salvar cálculo: {e}")
            raise
        finally:
            self.close()

    def buscar_calculos(self, tipo=None):
        """Retorna cálculos de fundações, filtrados por tipo, se fornecido"""
        self.connect()
        try:
            if tipo:
                self.cursor.execute("SELECT * FROM fundacoes WHERE tipo = ?", (tipo,))
            else:
                self.cursor.execute("SELECT * FROM fundacoes")
            resultados = self.cursor.fetchall()
            logging.info(f"{len(resultados)} cálculos encontrados.")
            return resultados
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar cálculos: {e}")
            raise
        finally:
            self.close()

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            logging.info("Conexão com o banco de dados SQLite encerrada.")
