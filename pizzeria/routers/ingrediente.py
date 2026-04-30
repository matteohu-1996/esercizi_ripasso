from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette import status

from database import get_db
from schemas.ingrediente import Ingrediente, IngredienteUpdate, IngredienteCreate
from crud import ingrediente as crud_ingrediente, ingrediente

router = APIRouter(
    prefix="/ingredienties",
    tags=["ingredienti"],
)

@router.get("/", response_model=List[Ingrediente])
def lista_ingredienti(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_ingrediente.get_ingredienti(db,skip,limit)

@router.get("/{ingrediente_id}", response_model=Ingrediente)
def ottieni_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    ingr = crud_ingrediente.get_ingrediente(db, ingrediente_id)
    if not ingr:
        raise HTTPException(
            status_code=404, detail=f"Ingrediente non trovato con ID {ingrediente_id}",
        )
    return ingr


@router.delete("/{ingrediente_id}", response_model=Ingrediente)
def elimina_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    ingr = crud_ingrediente.delete_ingrediente(db, ingrediente_id)
    if not ingr:
        raise HTTPException(
            status_code=404, detail="Ingrediente con ID {ingrediente_id} non eliminato",
        )
    return ingr


@router.post("/", response_model=Ingrediente, status_code=201)
def crea_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    return crud_ingrediente.create_ingrediente(db, ingrediente)

@router.put("/{ingrediente_id}", response_model=Ingrediente)
def aggiorna_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    ingr = crud_ingrediente.update_ingrediente(db, ingrediente_id, )
    if not ingr:
        raise HTTPException(
            status_code=404, detail="Ingrediente non trovato",
        )
    return ingr