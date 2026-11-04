from database import get_connection

def create_ponto(data_criacao, status, tipo_ponto, criador = "Nome do professor", responsavel = "Bruno Mars"): # cria um ponto e atribui um nome aleatório de responsável
    conn = get_connection ()                                                               # o ID é criado pelo banco de dados com auto increment
    try:
        conn.execute (
            """ INSERT INTO PONTO (data_criacao, status, tipo_ponto, criador, responsavel) 
            VALUES (?, ?, ?, ?, ?)
            """, (data_criacao, status, tipo_ponto, criador, responsavel)
        )
        conn.commit()
    finally:
        conn.close()


def get_pontos(): # consulta ponto no banco de dados
    conn = get_connection()
    try:
            pontos = conn.execute(
            """SELECT id, data_criacao, status, tipo_ponto, criador, responsavel
            FROM PONTO
            ORDER BY id DESC"""
        ). fetchall()
            return [dict(ponto) for ponto in pontos]
    finally:
            conn.close()