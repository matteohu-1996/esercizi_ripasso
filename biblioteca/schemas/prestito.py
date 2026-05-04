from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from models.prestito import StatoPrestito
from schemas.lettore import LettoreResponse
from schemas.libro import LibroResponse
from schemas.tag import TagResponse


class VocePrestitoCreate(BaseModel):
    libro_id: int
    quantita: int = Field(ge=1)
    tags_extra_ids: List[int] = []

class VocePrestitoResponse(BaseModel):
    voce_id: int
    libro: LibroResponse
    quantita: int
    tags_extra: List[TagResponse]

    class Config:
        from_attributes = True

class PrestitoCreate(BaseModel):
    lettore_id: int
    note: Optional[str] = None
    voci: List[VocePrestitoCreate]

class PrestitoStatoUpdate(BaseModel):
    stato: StatoPrestito

class PrestitoResponse(BaseModel):
    prestito_id: int
    data_ora: datetime
    stato: StatoPrestito
    note: Optional[str] = None
    lettore: LettoreResponse
    voci: List[VocePrestitoResponse]

    class Config:
        from_attributes =  True


class PrestitoList(BaseModel):
    prestito_id: int
    data_ora: datetime
    stato: StatoPrestito
    lettore: LettoreResponse

    class Config:
        from_attributes = True

class StoricoLettore(BaseModel):
    prestiti: List[PrestitoResponse]