from fastapi import APIRouter, Depends, HTTPException, Path
from app.schemas import FigurinhaSchema
from app.dependencies import pegar_sessao
from sqlalchemy.orm import Session
from app.models import Figurinha, Usuario
from app.routers.auth_routes import verificar_token

figurinhas_router = APIRouter(prefix="/figurinhas", tags=["Figurinha"])

@figurinhas_router.get("/listar")
async def listar_figurinhas(
    usuario: Usuario = Depends(verificar_token), 
    session: Session = Depends(pegar_sessao)):

    """
    Traz todas as figurinhas que pertencem ao ID do usuário que está logado
    """
     
    minhas_figurinhas = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id).all()

    # Utilizando List Comprehension para filtrar os dados em formato json
    return [
        {
            "sigla": figurinha.sigla,
            "numero": figurinha.numero,
            "quantidade": figurinha.quantidade,
            "observacao": figurinha.observacao
        }
        for figurinha in minhas_figurinhas
    ]

@figurinhas_router.post("/criar_figurinha")
async def criar_figurinha(
    figurinhaschema:FigurinhaSchema,  
    usuario: Usuario = Depends(verificar_token), 
    session: Session = Depends(pegar_sessao)):

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
async def remover_figurinha(
    figurinhaschema:FigurinhaSchema,
    usuario: Usuario = Depends(verificar_token), 
    session: Session = Depends(pegar_sessao)):

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
        
@figurinhas_router.get("/repetidas")
async def verificar_repetidas(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)):

    """
    Esta é a rota padrão de listagem de figurinhas repetidas, toda listagem de repetidas precisa de uma autenticação prévia!
    """
    figurinhas_repetidas = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id, Figurinha.quantidade > 1).all()
    
    # Utilizando List Comprehension para filtrar os dados em formato json
    return [
        
        {
            "sigla": figurinha.sigla,
            "numero": figurinha.numero,
            "quantidade": (figurinha.quantidade)-1,
            "observacao": figurinha.observacao
        }
        for figurinha in figurinhas_repetidas
    ]

@figurinhas_router.get("/progresso")
async def mostrar_progresso(
    usuario: Usuario = Depends(verificar_token), 
    session: Session = Depends(pegar_sessao)):

    """
    Esta é a rota padrão para listagem de progresso do album, a rota de listagem do progresso precisa de uma autenticação prévia!
    """
    TOTAL_ALBUM = 980
    quantidade_figurinhas  = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id).count()
    final_percentual = (quantidade_figurinhas/TOTAL_ALBUM) * 100
    return {
    "figurinhas": quantidade_figurinhas,
    "total_album": TOTAL_ALBUM,
    "progresso_percentual": round(final_percentual, 2)
        }

@figurinhas_router.get("/{sigla}/{numero}")
async def destacar_figurinha(
    sigla:str = Path(..., min_length=3, max_length=3, description="A sigla da seleção com 3 letras"), 
    numero:int = Path(..., ge=1, description="O número da figurinha deve ser maior ou igual a 1"),
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)):

    """
    Esta é a rota padrão para consulta detalhada de figurinha, a rota consulta detalhada precisa de uma autenticação prévia!
    """
    # Validando que a sigla sera maiuscula para consulta correta na tabela
    sigla_upper = sigla.upper()
    figurinha_destacada = session.query(Figurinha).filter(Figurinha.usuario_id == usuario.id, Figurinha.sigla==sigla_upper, Figurinha.numero==numero).first()
    if not figurinha_destacada:
        raise HTTPException(status_code=404, detail="Figurinha Não Encontrada")
    
    return {
    "sigla": figurinha_destacada.sigla,
    "numero": figurinha_destacada.numero,
    "observação": figurinha_destacada.observacao
            }
