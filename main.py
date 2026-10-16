from users import create_diretor # cria diretor
from users import create_user # cria outros usuários
import re # para verificar o e-mail

#cria diretor
def main_diretor ():
    name = input("Nome: ").strip.title() #nome com início com letra maiúscula
    email = input("E-mail: ").strip

    diretor = create_diretor(name, email)

    print(diretor)



#cria demais usuários
def main_user ():
    name = input("Nome: ").strip.title() # nome com início com letra maiúscula
    email = input("E-mail: ").strip()
    if not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email): # verifica se o e-mail tem enderço válido
        print("E-mail inválido")
        return
    role = [
        "Coordenador",
        "Agente de apoio",
        "Professor"
    ]
    telefone = input("Telefone: ").strip()
    if not name.strip.title() or not email.strip() or not telefone: # obriga o preenchimento dos campos, como o role é obrigatório da lista, ficou de fora aqui
        return "Todos os campos são obrigatórios"

    user = create_user(name, email, role, telefone)

    print("O seguinte usuário foi criado com sucesso: ", user)

if __name__ == "__main__":
    main_user()
    main_diretor()