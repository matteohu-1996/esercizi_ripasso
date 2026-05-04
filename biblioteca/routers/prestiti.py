from  fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.prestito import PrestitoCreate, PrestitoStatoUpdate, PrestitoResponse, PrestitoList
from crud import prestito as crud_prestito
from crud import lettore as crud_lettore
from dependecies import get_db

router = APIRouter(
    prefix="/prestiti",
    tags=["prestiti"],
)

@router.post("/", response_model=PrestitoResponse, status_code=201)
def create_prestito(prestito: PrestitoCreate, db: Session = Depends(get_db)):
    lettore = crud_lettore.get_lettore(db, prestito.lettore_id)
    if not lettore:
        raise HTTPException(status_code=404, detail="Lettore non trovato")
    return crud_prestito.create_prestito(db, prestito)


@router.patch("/{prestito_id}/stato", response_model=PrestitoResponse)
def aggiorna_stato(prestito_id: int, stato_update: PrestitoStatoUpdate, db: Session = Depends(get_db)):
    obj = crud_prestito.aggiorna_stato(db, prestito_id, stato_update)
    if not obj:
        raise HTTPException(status_code=404, detail="Prestito non trovato")
    return obj

@router.get("/oggi", response_model=List[PrestitoList])
def prestiti_oggi(db: Session = Depends(get_db)):
    return crud_prestito.get_prestiti_oggi(db)

@router.get("/{prestito_id}", response_model=PrestitoResponse)
def get_prestito(prestito_id: int, db: Session = Depends(get_db)):
    obj = crud_prestito.get_prestito(db, prestito_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Prestito con ID {prestito_id} non trovato")
    return obj

