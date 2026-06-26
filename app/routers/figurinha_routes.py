from fastapi import APIRouter, Depends
from app.schemas import FigurinhaSchema
from app.dependencies import pegar_sessao
from sqlalchemy.orm import Session
from app.models import Figurinha



figurinhas_router = APIRouter(prefix="/figurinhas", tags=["Figurinha"])

@figurinhas_router.get("/listar")
async def figurinhas():
    """
    Esta é a rota padrão de figurinhas, toda listagem de figurinhas precisa de uma autenticação prévia!
    """
    return {"Mensagem": "Você acessou seu album de figurinhas"}

@figurinhas_router.post("/criar_figurinha")
async def criar_figurinha(figurinhaschema:FigurinhaSchema, session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão de criação de figurinha, toda criação de figurinhas precisa de uma autenticação prévia!
    """
    figurinha = session.query(Figurinha).filter(Figurinha.sigla==figurinhaschema.sigla, Figurinha.numero==figurinhaschema.numero ).first()
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

    
