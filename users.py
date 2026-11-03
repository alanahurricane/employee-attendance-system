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

def edit_professor(email_antigo, email, nome, telefone, coordenacao): # edita as informações no banco de dados
      conn = get_connection() 
      try:
            conn.execute(
                  """UPDATE PROFESSOR
                  SET email = ?, nome = ?, telefone = ?, coordenacao = ?
                  WHERE email = ?""",
                  (email, nome, telefone, coordenacao, email_antigo)
            )
            conn.commit()
      finally:
        conn.close()

def erase_professor(email): # exclui professor do banco de dados
    conn = get_connection()
    try:
            resultado = conn.execute(
                  "DELETE FROM PROFESSOR WHERE email = ?",
                  (email,)
            )

            print("Linhas excluídas:", resultado.rowcount)

            conn.commit()
    finally:
            conn.close()
