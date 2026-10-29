import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "database.db"

def get_connection(): # abre conexão com o banco de dados
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row # permite acessar as colunas
    return conn
