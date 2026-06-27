from fastapi import Depends, HTTPException
from app.main import SECRET_KEY, ALGORITHM, oauth2_schema
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import Usuario
from jose import JWTError, jwt

# Criando uma dependencia para as rotas terem acesso ao DB.
def pegar_sessao():
    session = SessionLocal()
    try:
        # Yield permite entregar a sesão para a rota.
        # Após a rota terminar, o FastAPI retorna para esta função e executa o finally
        yield session
    
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, token expirado!")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario