from db import criar_conexao

def inserir_livro(título, autor):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO livros(título,autor)
    VALUES (?,?)               
    """, (título, autor))
    conexao.commit()
    conexao.close()

def listar_livros():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM livros")
    for livro in cursor.fetchall():
        print(livro)
    conexao.close()