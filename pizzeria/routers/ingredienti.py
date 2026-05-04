from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.ingrediente import IngredienteCreate, IngredienteUpdate, IngredienteResponse
from crud import ingrediente as crud_ingrediente
from dependencies import get_db

router = APIRouter(prefix="/ingredienti", tags=["ingredienti"])


@router.get("/", response_model=List[IngredienteResponse])
def list_ingredienti(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_ingrediente.get_ingredienti(db, skip=skip, limit=limit)


@router.get("/{ingrediente_id}", response_model=IngredienteResponse)
def get_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    obj = crud_ingrediente.get_ingrediente(db, ingrediente_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente non trovato")
    return obj


@router.post("/", response_model=IngredienteResponse, status_code=201)
def create_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    return crud_ingrediente.create_ingrediente(db, ingrediente)


@router.put("/{ingrediente_id}", response_model=IngredienteResponse)
def update_ingrediente(ingrediente_id: int, ingrediente: IngredienteUpdate, db: Session = Depends(get_db)):
    obj = crud_ingrediente.update_ingrediente(db, ingrediente_id, ingrediente)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente non trovato")
    return obj


@router.delete("/{ingrediente_id}", response_model=IngredienteResponse)
def delete_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    obj = crud_ingrediente.delete_ingrediente(db, ingrediente_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente non trovato")
    return obj
