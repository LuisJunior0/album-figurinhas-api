from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base  

class Figurinha(Base):
    __tablename__ = "figurinhas"
    
    # ID de autoincremento automatico
    id = Column(Integer, primary_key=True, index=True)

    # Siglas das seleções com limite de 3 caracteres
    sigla = Column(String(3), nullable=False)
    
    # Número da figurinha da seleção (de 0 a 20)
    numero = Column(Integer, nullable=False)
    
    # Quantidade de figurinhas coladas/repetidas (Assume valor padrão de 1)
    quantidade = Column(Integer, nullable=False, default=1)
    
    # Data e hora de quando a figurinha foi registrada 
    created_at = Column(DateTime, server_default=func.now())

class Usuario(Base):
    __tablename__ = "Usuario"