from pydantic import BaseModel
from typing import Optional, List


class OrdineBase(BaseModel):
    # roba base che sono semper richieste
    quantita : int

class OrdineCreate(OrdineBase):
    # roba che servono per costruire ordine nuovo per creazione e che non servono per lettura
    id_cliente: int
    id_pizza: int

class Ordine(OrdineBase):
    # informazioni per lettura
    ordine_id: int
    # non ereditare in OrdineCreate gli id
    id_cliente: int
    id_pizza: int

    class Config:
        from_attributes = True