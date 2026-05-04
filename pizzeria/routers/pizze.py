from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.pizza import PizzaCreate, PizzaUpdate, PizzaResponse
from crud import pizza as crud_pizza
from dependencies import get_db

router = APIRouter(prefix="/pizze", tags=["pizze"])


@router.get("/", response_model=List[PizzaResponse])
def list_pizze(
    skip: int = 0,
    limit: int = 100,
    vegetariane: Optional[bool] = Query(None, description="Filtra pizze 100% vegetariane"),
    senza_allergeni: Optional[bool] = Query(None, description="Filtra pizze senza allergeni"),
    nome: Optional[str] = Query(None, description="Ricerca parziale per nome (case-insensitive)"),
    db: Session = Depends(get_db),
):
    return crud_pizza.get_pizze(
        db, skip=skip, limit=limit,
        vegetariane=vegetariane, senza_allergeni=senza_allergeni, nome=nome
    )


@router.get("/{pizza_id}", response_model=PizzaResponse)
def get_pizza(pizza_id: int, db: Session = Depends(get_db)):
    obj = crud_pizza.get_pizza(db, pizza_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Pizza non trovata")
    return obj


@router.post("/", response_model=PizzaResponse, status_code=201)
def create_pizza(pizza: PizzaCreate, db: Session = Depends(get_db)):
    return crud_pizza.create_pizza(db, pizza)


@router.put("/{pizza_id}", response_model=PizzaResponse)
def update_pizza(pizza_id: int, pizza: PizzaUpdate, db: Session = Depends(get_db)):
    obj = crud_pizza.update_pizza(db, pizza_id, pizza)
    if not obj:
        raise HTTPException(status_code=404, detail="Pizza non trovata")
    return obj


@router.delete("/{pizza_id}", response_model=PizzaResponse)
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    obj = crud_pizza.delete_pizza(db, pizza_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Pizza non trovata")
    return obj
