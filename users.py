from database import get_connection

#cria diretor
def create_diretor(name, email):
    diretor = {
        "name": name,
        "email": email
    }

    return diretor


#cria outros usuários diretamente no banco de dados
def create_user(name, email, role, telefone):
    conn = get_connection ()
    conn.execute(
        """INSERT INTO users (name, email, role, telefone)
        VALUES (?, ?, ?, ?)
        """, (name, email, role, telefone))
    conn.commit()
    conn.close()

