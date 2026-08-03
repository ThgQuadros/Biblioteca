from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker


db = create_engine('sqlite:///exemplo.db')
Session = sessionmaker(bind=db)
session = Session()


Base = declarative_base()


#tabelas

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)

    def __int__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

class Livro(Base):

    __tablename__ = 'livro'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    titulo = Column('titulo', String)
    qtde_paginas = Column('qtde_paginas', Integer)
    dono = Column('dono', ForeignKey('usuarios.id'))

    def __int__(self, titulo, qtde_paginas, dono):
        self.titulo = titulo
        self.qtde_paginas = self.qtde_paginas
        self.dono = dono


Base.metadata.create_all(bind=db)

#Crud
#como criar um usuario

usuario = Usuario(nome = "joao", email="joao@hotmail.com", senha=123456)
session.add(usuario) #adiciona novo usuario na sessão
session.commit() # salvo o usuario no banco de dados

#usuario = Usuario(nome = "maria", email="maria@hotmail.com", senha=123456)
#session.add(usuario) #adiciona novo usuario na sessão
#session.commit() # salvo o usuario no banco de dados

# encontrar um usuario pelo id
usuario = session.query(Usuario).filter_by(id=1).first()
lista_usuario = session.query(Usuario).all()#lista todos os usuarios

#Crud
#como criar um livro

livro = Livro(titulo='O Senhor dos Anéis', qtde_paginas=1000, dono=1)
session.add(livro)#adiciona novo livro na sessão
session.commit()#salvo o livrono banco de dados

livro = Livro(titulo='O Hobbit', qtde_paginas=300, dono=1)
session.add(livro) #adiciona novo livro na sessão
session.commit()#salvo o livrono banco de dados