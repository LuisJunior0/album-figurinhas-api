from fastapi import APIRouter, Depends
from app.schemas import FigurinhaSchema
from app.dependencies import pegar_sessao
from sqlalchemy.orm import Session, session
from app.models import Figurinha, Usuario
from app.routers.auth_routes import verificar_token

figurinhas_router = APIRouter(prefix="/figurinhas", tags=["Figurinha"])

@figurinhas_router.get("/listar", response_model=list[str])
async def listar_figurinhas(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """
    Traz todas as figurinhas que pertencem ao ID do usuário que está logado
    """
    lista_formatada = []

    minhas_figurinhas = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id).all()
    
    for figurinha in minhas_figurinhas:
        texto = f"{figurinha.sigla} {figurinha.numero} -- {figurinha.quantidade}"
        lista_formatada.append(texto)
    
    return lista_formatada

@figurinhas_router.post("/criar_figurinha")
async def criar_figurinha(figurinhaschema:FigurinhaSchema, session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão de criação de figurinha, toda criação de figurinhas precisa de uma autenticação prévia!
    """
    figurinha = session.query(Figurinha).filter(Figurinha.sigla==figurinhaschema.sigla, Figurinha.numero==figurinhaschema.numero).first()
    if figurinha:
        #Ja existe uma figurinha com essa sigla e numero [!]
        figurinha.quantidade += figurinhaschema.quantidade
        figurinha.observacao = figurinhaschema.observacao
        session.commit()
        return {"mensagem": f"Figurinha repetida [!] adicionada com sucesso: {figurinhaschema.sigla, figurinhaschema.numero} [+{figurinhaschema.quantidade}]"}
    
    else:
        #figurinha nova encontrada [+]
        figurinha_nova = Figurinha(figurinhaschema.sigla, figurinhaschema.numero, figurinhaschema.observacao, figurinhaschema.usuario_id, figurinhaschema.quantidade)
        session.add(figurinha_nova)
        session.commit()
        return {"mensagem": f"Figurinha NOVA [+] cadastrada com SUCESSO:  {figurinhaschema.sigla, figurinhaschema.numero} [+{figurinhaschema.quantidade}]"}

    
