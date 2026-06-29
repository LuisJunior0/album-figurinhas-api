from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True

class FigurinhaSchema(BaseModel):
    sigla: str
    numero: int
    observacao: Optional[str] = None
    quantidade: int = Field(default = 1, ge=1)
    class Config:
        from_attributes = True
