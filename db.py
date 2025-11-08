# db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(BASE_DIR, exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "compras.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Solicitacao(Base):
    __tablename__ = "solicitacoes"
    id = Column(Integer, primary_key=True, index=True)
    solicitante = Column(String, nullable=False)
    item = Column(String, nullable=False)
    quantidade = Column(Integer, default=1)
    descricao = Column(Text)
    centro_custo = Column(String)
    prioridade = Column(String, default="Normal")  # Baixa/Normal/Alta
    status = Column(String, default="A FAZER")     # A FAZER, EM APROVACAO, APROVADO, REJEITADO, COMPRADO
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow)

    cotacoes = relationship("Cotacao", back_populates="solicitacao", cascade="all, delete-orphan")
    anexos = relationship("Anexo", back_populates="solicitacao", cascade="all, delete-orphan")
    historico = relationship("Historico", back_populates="solicitacao", cascade="all, delete-orphan")

class Cotacao(Base):
    __tablename__ = "cotacoes"
    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"))
    fornecedor = Column(String)
    preco_unitario = Column(Float)
    quantidade = Column(Integer, default=1)
    prazo = Column(String)
    observacao = Column(Text)

    solicitacao = relationship("Solicitacao", back_populates="cotacoes")

class Anexo(Base):
    __tablename__ = "anexos"
    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"))
    filename = Column(String)
    filepath = Column(String)

    solicitacao = relationship("Solicitacao", back_populates="anexos")

class Historico(Base):
    __tablename__ = "historico"
    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"))
    acao = Column(String)
    comentario = Column(Text)
    autor = Column(String)
    data = Column(DateTime, default=datetime.utcnow)

    solicitacao = relationship("Solicitacao", back_populates="historico")

def get_session():
    return SessionLocal()
