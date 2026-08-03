from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine("sqlite:///exemplo.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

#tabelas

class Usuario(Base):

    __tablename__ = "cadastrar_usuario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    matricula = Column("matricula", String)

    def __init__(self, nome=True, matricula=True, ativo=True):
        self.nome = nome
        self.matricula = matricula

class Livro(Base):

    __tablename__ = "cadastrar_livros"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String)
    qtde_paginas = Column("qtde_paginas", Integer)
    dono = Column("dono", ForeignKey("usuarios.id"))

    def __init__(self, codigo_livro=True, titulo=True, autor=True):
        self.codigo_livro = codigo_livro
        self.titulo = titulo
        self.autor = autor

Base.metadata.create_all(bind=db)