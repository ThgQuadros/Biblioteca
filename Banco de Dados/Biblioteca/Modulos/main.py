import json
import os

ARQUIVO_LIVROS = "livros.json"
ARQUIVO_USUARIOS = "usuarios.json"

def carregar_arquivo(nome):
    if os.path.exists(nome):
        with open(nome, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []

def salvar_arquivo(nome, dados):
    with open(nome, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

livros = carregar_arquivo(ARQUIVO_LIVROS)
usuarios = carregar_arquivo(ARQUIVO_USUARIOS)

def cadastrar_livro():
    print("\nCADASTRO DE LIVRO")
    codigo = input("Código: ")
    titulo = input("Título: ")
    autor = input("Autor: ")
    livro = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "emprestado": False
    }
    livros.append(livro)
    salvar_arquivo(ARQUIVO_LIVROS, livros)
    print("Livro cadastrado com sucesso!")

def listar_livros():
    print("\nLISTA DE LIVROS")
    if len(livros) == 0:
        print("Nenhum livro cadastrado.")
        return
    for livro in livros:
        status = "Emprestado" if livro["emprestado"] else "Disponível"
        print("-" * 40)
        print("Código:", livro["codigo"])
        print("Título:", livro["titulo"])
        print("Autor:", livro["autor"])
        print("Status:", status)

def cadastrar_usuario():
    print("\nCADASTRO DE USUÁRIO")
    matricula = input("Matrícula: ")
    nome = input("Nome: ")
    usuario = {
        "matricula": matricula,
        "nome": nome
    }
    usuarios.append(usuario)
    salvar_arquivo(ARQUIVO_USUARIOS, usuarios)
    print("Usuário cadastrado com sucesso!")

def listar_usuarios():
    print("\nUSUÁRIOS")
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(usuario["matricula"], "-", usuario["nome"])

def emprestar_livro():
    codigo = input("Código do livro: ")
    for livro in livros:
        if livro["codigo"] == codigo:
            if livro["emprestado"]:
                print("Livro já emprestado.")
                return
            matricula = input("Matrícula do usuário: ")
            livro["emprestado"] = True
            livro["usuario"] = matricula
            salvar_arquivo(ARQUIVO_LIVROS, livros)
            print("Empréstimo realizado.")
            return
    print("Livro não encontrado.")

def devolver_livro():
    codigo = input("Código do livro: ")
    for livro in livros:
        if livro["codigo"] == codigo:
            livro["emprestado"] = False
            if "usuario" in livro:
                del livro["usuario"]
            salvar_arquivo(ARQUIVO_LIVROS, livros)
            print("Livro devolvido.")
            return
    print("Livro não encontrado.")

def pesquisar_livro():
    termo = input("Digite o título: ").lower()
    encontrou = False
    for livro in livros:
        if termo in livro["titulo"].lower():
            print("\nLivro Encontrado")
            print("Código:", livro["codigo"])
            print("Título:", livro["titulo"])
            print("Autor:", livro["autor"])
            encontrou = True
    if not encontrou:
        print("Nenhum livro encontrado.")

def relatorio():
    total = len(livros)
    emprestados = 0
    for livro in livros:
        if livro["emprestado"]:
            emprestados += 1
    disponiveis = total - emprestados
    print("\nRELATÓRIO")
    print("Total de Livros:", total)
    print("Disponíveis:", disponiveis)
    print("Emprestados:", emprestados)

while True:
    print("\n")
    print("=" * 50)
    print(" SISTEMA DE BIBLIOTECA ")
    print("=" * 50)
    print("1 - Cadastrar Livro")
    print("2 - Listar Livros")
    print("3 - Cadastrar Usuário")
    print("4 - Listar Usuários")
    print("5 - Emprestar Livro")
    print("6 - Devolver Livro")
    print("7 - Pesquisar Livro")
    print("8 - Relatório")
    print("0 - Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_livro()
    elif opcao == "2":
        listar_livros()
    elif opcao == "3":
        cadastrar_usuario()
    elif opcao == "4":
        listar_usuarios()
    elif opcao == "5":
        emprestar_livro()
    elif opcao == "6":
        devolver_livro()
    elif opcao == "7":
        pesquisar_livro()
    elif opcao == "8":
        relatorio()
    elif opcao == "0":
        print("Sistema encerrado.")
        break
    else:
        print("Opção inválida.")