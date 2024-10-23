import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'lct_calculator.db')

def connect_db():
    """Estabelece conexão com o banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    """Cria tabelas necessárias para armazenar dados de fundações, relatórios e sincronização BIM"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fundacoes (
            id INTEGER PRIMARY KEY,
            tipo TEXT NOT NULL,
            base REAL,
            altura REAL,
            fck REAL,
            esforco REAL,
            resultado REAL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY,
            fundacao_id INTEGER,
            caminho_arquivo TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(fundacao_id) REFERENCES fundacoes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sincronizacao_bim (
            id INTEGER PRIMARY KEY,
            fundacao_id INTEGER,
            status TEXT,
            sincronizado_em TIMESTAMP,
            FOREIGN KEY(fundacao_id) REFERENCES fundacoes(id)
        )
    ''')

    conn.commit()
    conn.close()

# Exemplo de uso, cria as tabelas ao rodar o script
if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso.")
