from pydantic import BaseModel, Field
from typing import Optional, List

class LettoreBase(BaseModel):
    nome: str
    email: str
    telefono: str

class LettoreCreate(LettoreBase):
    pass

class LettoreUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = Field(default=None, min_length=1)

class LettoreResponse(LettoreBase):
    lettore_id: int

    class Config:
        from_attributes = True