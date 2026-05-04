from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from schemas.ordine import StoricoCliente
from crud import cliente as crud_cliente
from crud import ordine as crud_ordine
from dependencies import get_db

router = APIRouter(prefix="/clienti", tags=["clienti"])


@router.get("/", response_model=List[ClienteResponse])
def list_clienti(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_cliente.get_clienti(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    obj = crud_cliente.get_cliente(db, cliente_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    return obj


@router.post("/", response_model=ClienteResponse, status_code=201)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crud_cliente.create_cliente(db, cliente)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    obj = crud_cliente.update_cliente(db, cliente_id, cliente)
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    return obj


@router.delete("/{cliente_id}", response_model=ClienteResponse)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    obj = crud_cliente.delete_cliente(db, cliente_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    return obj


@router.get("/{cliente_id}/storico", response_model=StoricoCliente)
def storico_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    ordini, totale = crud_ordine.get_storico_cliente(db, cliente_id)
    return StoricoCliente(ordini=ordini, totale_speso=totale)
