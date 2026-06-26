from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
# Criptografia das senhas do DB
SECRET_KEY = os.getenv("SECRET_KEY")


from app.database import engine, Base  
from app import models 

# Lê todas as classes que herdam de 'Base' e cria as tabelas reais no PostgreSQL usando o 'engine'
Base.metadata.create_all(bind=engine)

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from app.routers.figurinha_routes import figurinhas_router
from app.routers.auth_routes import auth_router

app.include_router(figurinhas_router)
app.include_router(auth_router)