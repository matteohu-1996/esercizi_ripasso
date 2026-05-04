from pydantic import BaseModel, Field
from typing import Optional


class ClienteBase(BaseModel):
    nome: str
    telefono: str = Field(min_length=1)
    indirizzo: str


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefono: Optional[str] = Field(default=None, min_length=1)
    indirizzo: Optional[str] = None


class ClienteResponse(ClienteBase):
    cliente_id: int

    class Config:
        from_attributes = True
