from fastapi import APIRouter

figurinhas_router = APIRouter(prefix="/figurinhas", tags=["Figurinha"])

@figurinhas_router.get("/")
async def figurinhas():
    """
    Esta é a rota padrão de figurinhas, toda listagem de figurinhas precisa de uma autenticação prévia!
    """
    return {"Mensagem": "Você acessou seu album de figurinhas"}