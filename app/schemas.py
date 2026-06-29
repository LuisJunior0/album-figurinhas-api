from pydantic import BaseModel, EmailStr, Field, field_validator
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
    sigla: str = Field(pattern=r"^[a-zA-Z]{3}$")
    numero: int = Field(ge=1, le=20)
    quantidade: int = Field(default = 1, ge=1)
    observacao: Optional[str] = Field(default=None, max_length=255)
    # Usuario pode passar a sigla minusculo ou maiusculo, porém apenas será salvo em upper
    @field_validator("sigla")
    @classmethod
    def transformar_em_maiusculo(cls, v: str) -> str:
        return v.upper()
    
    class Config:
        from_attributes = True
