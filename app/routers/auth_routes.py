from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/")
async def Autenticar():
    """
    Esta é a rota padrão de autenticação do sistema
    """
    return {"Mensagem": "Você acessou o login", "Autenticado": False}

