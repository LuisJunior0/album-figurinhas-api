from pydantic import BaseModel

class FigurinhaCreate_Schema(BaseModel):
    sigla: str
    numero: int
    quantidade: int