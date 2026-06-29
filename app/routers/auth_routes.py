from fastapi import APIRouter, Depends, HTTPException
from app.models import Usuario
from app.dependencies import pegar_sessao, verificar_token
from app.main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.schemas import  UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

def criar_token(
    usuario_id, 
    duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(usuario_id), "exp": data_expiracao}
    jwt_decodificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_decodificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Esta é a rota padrão de autenticação do sistema
    """
    return {"Mensagem": "Você acessou o login", "Autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(
    usuario_schema: UsuarioSchema, 
    session: Session = Depends(pegar_sessao)):

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

# Login -> email e senha > token JWT
@auth_router.post("/login")
async def login(
    loginschema: LoginSchema, 
    session: Session = Depends(pegar_sessao)):

    usuario = autenticar_usuario(loginschema.email, loginschema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario Não Encontrado ou Credenciais Invalidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }

@auth_router.post("/login_form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario Não Encontrado ou Credenciais Invalidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
            }