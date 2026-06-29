from fastapi import APIRouter, Depends, HTTPException
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
    if not minhas_figurinhas:
        raise HTTPException(status_code=404, detail="Figurinha Não Encontrada")
    
    for figurinha in minhas_figurinhas:
        texto = f"{figurinha.sigla} {figurinha.numero} -- {figurinha.quantidade}"
        lista_formatada.append(texto)
    
    return lista_formatada

@figurinhas_router.post("/criar_figurinha")
async def criar_figurinha(figurinhaschema:FigurinhaSchema,  usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão de criação de figurinha, toda criação de figurinhas precisa de uma autenticação prévia!
    """
    figurinha = session.query(Figurinha).filter(Figurinha.sigla==figurinhaschema.sigla, Figurinha.numero==figurinhaschema.numero, Figurinha.usuario_id==usuario.id).first()
    if figurinha:
        #Ja existe uma figurinha com essa sigla e numero [!]
        figurinha.quantidade += figurinhaschema.quantidade
        figurinha.observacao = figurinhaschema.observacao
        session.commit()
        return {"mensagem": f"Figurinha repetida [!] adicionada com SUCESSO: {figurinhaschema.sigla, figurinhaschema.numero} [+{figurinhaschema.quantidade}]"}
    
    else:
        #figurinha nova encontrada [+]
        # Devem ser passados os parametros na mesma ordem do __init__ em app.models para classe Figurinha
        # Ou definir antes o nome da variavel igual ao construtor __init__
        figurinha_nova = Figurinha(sigla=figurinhaschema.sigla, numero=figurinhaschema.numero, observacao=figurinhaschema.observacao, usuario_id=usuario.id, quantidade= figurinhaschema.quantidade)
        session.add(figurinha_nova)
        session.commit()
        return {"mensagem": f"Figurinha NOVA [+] cadastrada com SUCESSO:  {figurinhaschema.sigla, figurinhaschema.numero} [+{figurinhaschema.quantidade}]"}

@figurinhas_router.post("/remover_figurinha")
async def remover_figurinha(figurinhaschema:FigurinhaSchema, usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    figurinha_removida = session.query(Figurinha).filter(Figurinha.sigla==figurinhaschema.sigla, Figurinha.numero==figurinhaschema.numero, Figurinha.usuario_id==usuario.id).first()
    if not figurinha_removida:
        raise HTTPException(status_code=404, detail="Figurinha Não Encontrada")
    elif figurinha_removida.quantidade > figurinhaschema.quantidade:
        # Não deletar uma linha, apenas diminuir a quantidade
        figurinha_removida.quantidade -= figurinhaschema.quantidade
        session.commit()
        return {"mensagem": f"Figurinha(s) removida [!] com SUCESSO: {figurinhaschema.sigla, figurinhaschema.numero} [-{figurinhaschema.quantidade}]"}
    else:
        # Se o numero a remover for maior ou igual que a quantidade, deletar a linha do banco de dados
        session.delete(figurinha_removida)
        session.commit()
        return {"mensagem": f"Figurinha Deletada [-] do Album: {figurinhaschema.sigla, figurinhaschema.numero}"}
        



    
