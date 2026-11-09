from database import get_connection

def create_ponto(data_criacao, status, tipo_ponto, criador, responsavel = "Nome do responsável"): # cria um ponto e atribui um nome aleatório de responsável
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

def get_pontos(): # consulta os pontos de todos os professores
    conn = get_connection()

    try:
        pontos = conn.execute(
            """SELECT
                PONTO.id,
                PONTO.data_criacao,
                PONTO.status,
                PONTO.tipo_ponto,
                COALESCE(PROFESSOR.nome, PONTO.criador) AS criador,
                PONTO.responsavel
            FROM PONTO
            LEFT JOIN PROFESSOR
                ON PONTO.criador = PROFESSOR.email
            ORDER BY PONTO.id DESC"""
        ).fetchall()

        return [dict(ponto) for ponto in pontos]

    finally:
        conn.close()


def get_pontos_professor(email): # consulta os pontos do próprio professor
    conn = get_connection()
    try:
        pontos = conn.execute(
            """SELECT id, data_criacao, status, tipo_ponto
            FROM PONTO
            WHERE criador = ?
            ORDER BY id DESC""",
            (email,)
        ).fetchall()

        return [dict(ponto) for ponto in pontos]
    finally:
        conn.close()
