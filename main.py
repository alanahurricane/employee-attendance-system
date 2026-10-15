from users import create_diretor #cria diretor
from users import create_user #cria outros usuários

#cria diretor
def main ():
    name = input("Nome: ")
    email = input("E-mail: ")

    diretor = create_diretor(name, email)

    print(diretor)

if __name__ == "__main__":
    main()



#cria demais usuários
def main ():
    name = input("Nome: ")
    email = input("E-mail: ")
    role = [
        "Coordenador",
        "Agente de apoio",
        "Professor"
    ]
    telefone = input("Telefone: ")

    user = create_user(name, email, role, telefone)

    print(user)

if __name__ == "__main__":
    main()
