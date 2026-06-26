from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class FigurinhaSchema(BaseModel):
    sigla: str
    numero: int
    observacao: Optional[str] = None
    quantidade: int
    usuario_id: int
    
    

    class Config:
        from_attributes = True