from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.ordine import OrdineCreate, OrdineStatoUpdate, OrdineResponse, OrdineList
from crud import ordine as crud_ordine
from crud import cliente as crud_cliente
from dependencies import get_db

router = APIRouter(prefix="/ordini", tags=["ordini"])


@router.post("/", response_model=OrdineResponse, status_code=201)
def create_ordine(ordine: OrdineCreate, db: Session = Depends(get_db)):
    cliente = crud_cliente.get_cliente(db, ordine.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    return crud_ordine.create_ordine(db, ordine)


@router.get("/oggi", response_model=List[OrdineList])
def ordini_oggi(db: Session = Depends(get_db)):
    return crud_ordine.get_ordini_oggi(db)


@router.get("/{ordine_id}", response_model=OrdineResponse)
def get_ordine(ordine_id: int, db: Session = Depends(get_db)):
    obj = crud_ordine.get_ordine(db, ordine_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    return obj


@router.patch("/{ordine_id}/stato", response_model=OrdineResponse)
def aggiorna_stato(ordine_id: int, stato_update: OrdineStatoUpdate, db: Session = Depends(get_db)):
    obj = crud_ordine.aggiorna_stato(db, ordine_id, stato_update)
    if not obj:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    return obj
