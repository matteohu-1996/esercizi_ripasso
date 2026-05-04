from pydantic import BaseModel
from typing import List, Optional
from schemas.ingrediente import IngredienteResponse


class PizzaBase(BaseModel):
    nome: str
    prezzo_base: float
    descrizione: Optional[str] = None
    disponibile: bool = True


class PizzaCreate(PizzaBase):
    ingredienti_ids: List[int] = []


class PizzaUpdate(BaseModel):
    nome: Optional[str] = None
    prezzo_base: Optional[float] = None
    descrizione: Optional[str] = None
    disponibile: Optional[bool] = None
    ingredienti_ids: Optional[List[int]] = None


class PizzaResponse(PizzaBase):
    pizza_id: int
    prezzo_totale: float
    ingredienti: List[IngredienteResponse] = []

    class Config:
        from_attributes = True
