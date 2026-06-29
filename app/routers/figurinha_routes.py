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
        figurinha_nova = Figurinha(sigla=figurinhaschema.sigla, numero=figurinhaschema.numero, quantidade= figurinhaschema.quantidade, usuario_id=usuario.id, observacao=figurinhaschema.observacao)
        session.add(figurinha_nova)
        session.commit()
        return {"mensagem": f"Figurinha NOVA [+] cadastrada com SUCESSO:  {figurinhaschema.sigla, figurinhaschema.numero} [+{figurinhaschema.quantidade}]"}

@figurinhas_router.post("/remover_figurinha")
async def remover_figurinha(figurinhaschema:FigurinhaSchema, usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão de remoção de figurinha, toda remoção de figurinha precisa de uma autenticação prévia!
    """
    figurinha_removida = session.query(Figurinha).filter(Figurinha.sigla==figurinhaschema.sigla, Figurinha.numero==figurinhaschema.numero, Figurinha.usuario_id==usuario.id).first()
    if not figurinha_removida:
        raise HTTPException(status_code=404, detail="Figurinha Não Encontrada") 
    elif figurinha_removida.quantidade > figurinhaschema.quantidade:
        # Não deletar uma linha, apenas diminuir a quantidade
        figurinha_removida.quantidade -= figurinhaschema.quantidade
        session.commit()
        return {"mensagem": f"Figurinha(s) removida [!] com SUCESSO: {figurinhaschema.sigla, figurinhaschema.numero} [-{figurinhaschema.quantidade}]"}
    else:
        # Se o numero a remover for maior que a quantidade, status 400 quantidade indisponivel para retirada
        if figurinha_removida.quantidade < figurinhaschema.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade maior que a disponível")
        
        else:
             # Se o numero a remover for igual a quantidade, deletar a linha do banco de dados
            session.delete(figurinha_removida)
            session.commit()
            return {"mensagem": f"Figurinha Deletada [-] do Album: {figurinhaschema.sigla, figurinhaschema.numero}"}
        
@figurinhas_router.get("/repetidas", response_model=list[str])
async def verificar_repetidas(usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão de listagem de figurinhas repetidas, toda listagem de repetidas precisa de uma autenticação prévia!
    """
    figurinhas_repetidas = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id, Figurinha.quantidade > 1).all()

    lista_repetidas = []
    for repetida in figurinhas_repetidas:
        texto = f"{repetida.sigla} {repetida.numero} -- {(repetida.quantidade) -1}"
        lista_repetidas.append(texto)
    return lista_repetidas
    

@figurinhas_router.get("/progresso")
async def mostrar_progresso(usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """
    Esta é a rota padrão para listagem de progresso do album, a rota de listagem do progresso precisa de uma autenticação prévia!
    """
    TOTAL_ALBUM = 980
    quantidade_figurinhas  = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id).count()
    final_percentual = (quantidade_figurinhas/TOTAL_ALBUM) * 100
    return {
    "figurinhas": quantidade_figurinhas,
    "total_album": TOTAL_ALBUM,
    "progresso percentual": round(final_percentual, 2)
        }

    
