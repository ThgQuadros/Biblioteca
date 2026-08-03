import sqlite3
from pathlib import Path

# Caminho do banco (na raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "biblioteca.db"


def conectar():
    """Retorna uma conexão com o banco SQLite."""
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    """Cria as tabelas compatíveis com a aplicação Flask."""
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        codigo TEXT PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano INTEGER,
        emprestado INTEGER NOT NULL DEFAULT 0,
        usuario_matricula TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livro_codigo TEXT NOT NULL,
        usuario_matricula TEXT NOT NULL,
        data_emprestimo TEXT NOT NULL,
        data_devolucao TEXT,
        FOREIGN KEY (livro_codigo) REFERENCES livros(codigo),
        FOREIGN KEY (usuario_matricula) REFERENCES usuarios(matricula)
    )
    """)

    conn.commit()
    conn.close()