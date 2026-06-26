from fastapi import APIRouter, Depends, HTTPException
from app.models import Usuario
from app.dependencies import pegar_sessao
from app.main import bcrypt_context
from app.schemas import  UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/")
async def home():
    """
    Esta é a rota padrão de autenticação do sistema
    """
    return {"Mensagem": "Você acessou o login", "Autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #Ja existe um usuario com esse email
        raise HTTPException(status_code=400, detail="Email do usuario ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuario cadastrado com sucesso, email: {usuario_schema.email}"}
