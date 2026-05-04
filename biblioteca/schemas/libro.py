from pydantic import BaseModel
from typing import List, Optional

from schemas.tag import TagResponse


class Libro(BaseModel):
    titolo: str
    isbn: str
    anno: int
    descrizione: Optional[str] = None
    durata_base: int
    disponibile: bool = True

class LibroCreate(BaseModel):
    tags_id: List[int] = []



class LibroUpdate(BaseModel):
    titolo: Optional[str] = None
    isbn: Optional[str] = None
    anno: Optional[int] = None
    descrizione: Optional[bool] = None
    durata_base: Optional[int] = None
    disponibile: Optional[bool] = None

class LibroResponse(BaseModel):
    libro_id: int
    titolo: str
    isbn: str
    anno: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True