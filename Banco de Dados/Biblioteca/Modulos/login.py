usuarios = {
    "admin": "123",
    "bibliotecario": "456",
    "aluno": "789"
}

def fazer_login():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    if usuario in usuarios and usuarios[usuario] == senha:
        print("Login realizado")
        return usuario
    else:
        print("Acesso negado")
        return None