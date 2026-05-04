from typing import List, Optional
from pydantic import  BaseModel

class TagBase(BaseModel):
    nome: str
    giorni_extra: Optional[int]
    riservato: bool = False
    didattico: bool = False


class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    nome: Optional[str] = None
    giorni_extra: Optional[int] = None
    riservato: Optional[bool] = None
    didattico: Optional[bool] = None

class TagResponse(TagBase):
    tag_id: int

    class Config:
        from_attributes = True