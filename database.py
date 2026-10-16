import sqlite3


def get_connection(): # abre conexão com o banco de dados
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row # permite acessar as colunas
    return conn
