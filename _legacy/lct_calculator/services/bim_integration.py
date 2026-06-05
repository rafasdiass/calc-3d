import sqlite3
from .sqlite_service import connect_db
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

def sincronizar_bim(fundacao_id: int) -> None:
    """
    Simula uma sincronização com a plataforma BIM e atualiza o status da fundação no banco de dados.

    :param fundacao_id: ID da fundação a ser sincronizada.
    """
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Simula sincronização com plataforma BIM
        status = "Sincronizado"
        
        # Atualiza o status de sincronização no banco de dados
        cursor.execute('''
            INSERT INTO sincronizacao_bim (fundacao_id, status, sincronizado_em)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (fundacao_id, status))

        conn.commit()
        logging.info(f"Fundação {fundacao_id} sincronizada com sucesso na plataforma BIM.")
    except Exception as e:
        logging.error(f"Erro ao sincronizar a fundação {fundacao_id}: {e}")
        raise
    finally:
        conn.close()
