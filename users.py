from database import get_connection

# cria um professor no banco de dados
def create_professor(email, nome, telefone, coordenacao):
    conn = get_connection ()
    try:
        conn.execute(
            """INSERT INTO PROFESSOR (email, nome, telefone, coordenacao)
            VALUES (?, ?, ?, ?)
            """, (email, nome, telefone, coordenacao))
        conn.commit()
    finally:
        conn.close()

def get_professores(): # consulta um professor no banco de dados
    conn = get_connection()
    try:
            professores = conn.execute(
            """SELECT email, nome, telefone, coordenacao
            FROM PROFESSOR
            ORDER BY nome"""
        ). fetchall()
            return [dict(professor) for professor in professores]
    finally:
            conn.close()
