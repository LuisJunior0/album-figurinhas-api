from app.database import engine
from sqlalchemy.orm import sessionmaker

# Criando uma dependencia para as rotas terem acesso ao DB.
def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    
    finally:
        session.close()