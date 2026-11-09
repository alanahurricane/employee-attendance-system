from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

# cria um professor no banco de dados
def create_professor(email, nome, telefone, coordenacao, senha):
    conn = get_connection()
    try:
        senha_hash = generate_password_hash(senha)

        conn.execute(
            """INSERT INTO PROFESSOR
            (email, nome, telefone, coordenacao, senha)
            VALUES (?, ?, ?, ?, ?)""",
            (email, nome, telefone, coordenacao, senha_hash)
        )
        conn.commit()
    finally:
        conn.close()


def get_professores():  # consulta os professores no banco de dados
    conn = get_connection()
    try:
        professores = conn.execute(
            """SELECT email, nome, telefone, coordenacao
            FROM PROFESSOR
            ORDER BY nome"""
        ).fetchall()

        return [dict(professor) for professor in professores]
    finally:
        conn.close()


def edit_professor(email_antigo, email, nome, telefone, coordenacao): # edita o professor
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


def erase_professor(email): # apaga o professor
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

def verify_login(email, senha): # verifica o login do professor
    conn = get_connection()

    try:
        professor = conn.execute(
            "SELECT senha FROM PROFESSOR WHERE email = ?",
            (email,)
        ).fetchone()

        if professor is None:
            return False

        senha_hash = professor["senha"]

        if not senha_hash:
            return False

        return check_password_hash(senha_hash, senha)

    finally:
        conn.close()
