
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega as variáveis do arquivo .env
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


# Criação a ULR para conexão com o banco de dados segura
DataBase_SQLAlchemy_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Criação do motor de conexão usando a ULR feita acima
engine = create_engine(DataBase_SQLAlchemy_URL)

# Sessões para conversa com o DataBase
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base que as demais irão herdar (subclasses)
Base = declarative_base()