# app.py
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from Biblioteca.Modulos.db_unificado import conectar, criar_tabelas

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "Biblioteca" / "templates"))

# garante que as tabelas existem ao iniciar o servidor
criar_tabelas()

@app.route("/")
def home():
    return render_template("index.html")

# ----------------- LIVROS ----------------

@app.route("/livros")
def listar_livros():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT codigo, titulo, autor, ano, emprestado, usuario_matricula
        FROM livros
        ORDER BY titulo
    """)
    livros = cur.fetchall()
    conn.close()
    # livros será uma lista de tuplas: (codigo, titulo, autor, ano, emprestado, usuario_matricula)
    return render_template("livros.html", livros=livros)

@app.route("/livros/novo", methods=["GET", "POST"])
def novo_livro():
    if request.method == "POST":
        codigo = request.form["codigo"].strip()
        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        ano = request.form.get("ano", "").strip()

        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO livros (codigo, titulo, autor, ano)
                VALUES (?, ?, ?, ?)
            """, (codigo, titulo, autor, ano or None))
            conn.commit()
        except Exception as e:
            conn.close()
            # ideal: mostrar mensagem de erro na página
            return f"Erro ao cadastrar livro: {e}", 400
        conn.close()
        return redirect(url_for("listar_livros"))

    return render_template("novo_livro.html")

# ----------------- USUÁRIOS ----------------

@app.route("/usuarios")
def listar_usuarios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT matricula, nome, email, telefone
        FROM usuarios
        ORDER BY nome
    """)
    usuarios = cur.fetchall()
    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        matricula = request.form["matricula"].strip()
        nome = request.form["nome"].strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()

        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO usuarios (matricula, nome, email, telefone)
                VALUES (?, ?, ?, ?)
            """, (matricula, nome, email or None, telefone or None))
            conn.commit()
        except Exception as e:
            conn.close()
            return f"Erro ao cadastrar usuário: {e}", 400
        conn.close()
        return redirect(url_for("listar_usuarios"))

    return render_template("novo_usuario.html")

# ----------------- EMPRÉSTIMOS ----------------

@app.route("/emprestimos/novo", methods=["GET", "POST"])
def novo_emprestimo():
    conn = conectar()
    cur = conn.cursor()

    # para montar selects, carregamos livros e usuários
    cur.execute("SELECT codigo, titulo FROM livros ORDER BY titulo")
    livros = cur.fetchall()
    cur.execute("SELECT matricula, nome FROM usuarios ORDER BY nome")
    usuarios = cur.fetchall()
    conn.close()

    if request.method == "POST":
        codigo = request.form["codigo_livro"].strip()
        matricula = request.form["matricula_usuario"].strip()

        conn = conectar()
        cur = conn.cursor()

        # verifica livro
        cur.execute("SELECT emprestado FROM livros WHERE codigo = ?", (codigo,))
        row = cur.fetchone()
        if row is None:
            conn.close()
            return "Livro não encontrado.", 404
        if row[0] == 1:
            conn.close()
            return "Livro já está emprestado.", 400

        # verifica usuário
        cur.execute("SELECT matricula FROM usuarios WHERE matricula = ?", (matricula,))
        user = cur.fetchone()
        if user is None:
            conn.close()
            return "Usuário não encontrado.", 404

        data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # grava empréstimo e atualiza livro
        cur.execute("""
            INSERT INTO emprestimos (livro_codigo, usuario_matricula, data_emprestimo)
            VALUES (?, ?, ?)
        """, (codigo, matricula, data_emprestimo))
        cur.execute("""
            UPDATE livros
            SET emprestado = 1, usuario_matricula = ?
            WHERE codigo = ?
        """, (matricula, codigo))

        conn.commit()
        conn.close()
        return redirect(url_for("listar_livros"))

    # GET: mostra formulário com listas de livros/usuários
    return render_template("novo_emprestimo.html", livros=livros, usuarios=usuarios)

@app.route("/emprestimos/devolver", methods=["GET", "POST"])
def devolver_livro():
    if request.method == "POST":
        codigo = request.form["codigo_livro"].strip()

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT emprestado FROM livros WHERE codigo = ?", (codigo,))
        row = cur.fetchone()
        if row is None:
            conn.close()
            return "Livro não encontrado.", 404
        if row[0] == 0:
            conn.close()
            return "Livro já está disponível.", 400

        data_devolucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            UPDATE emprestimos
            SET data_devolucao = ?
            WHERE livro_codigo = ? AND data_devolucao IS NULL
        """, (data_devolucao, codigo))

        cur.execute("""
            UPDATE livros
            SET emprestado = 0, usuario_matricula = NULL
            WHERE codigo = ?
        """, (codigo,))

        conn.commit()
        conn.close()
        return redirect(url_for("listar_livros"))

    # GET: só um form simples com campo código
    return render_template("devolver_livro.html")

# ----------------- RELATÓRIO ----------------

@app.route("/relatorio")
def relatorio():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM livros")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM livros WHERE emprestado = 1")
    emprestados = cur.fetchone()[0]

    disponiveis = total - emprestados

    conn.close()

    # você pode exibir isso em HTML
    return render_template(
        "relatorio.html",
        total=total,
        emprestados=emprestados,
        disponiveis=disponiveis,
    )

if __name__ == "__main__":
    app.run(debug=True)