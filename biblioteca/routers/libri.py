from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import Optional, List
from schemas.libro import LibroCreate, LibroUpdate, LibroResponse
from crud import libro as crud_libro
from dependecies import get_db

router = APIRouter(
    prefix="/libri",
    tags=["libri"],
)

@router.get("/", response_model=List[LibroResponse])
def list_libri(
    skip: int = 0,
    limit: int = 100,
    didattici: Optional[bool] = Query(None, description="Filtra libri per 100% didattici "),
    senza_riservati: Optional[bool] = Query(None, description="Filtra libri senza tag riservati"),
    titolo: Optional[str] = Query(None, description="Ricerca parziale per titolo (case-insensitive)"),
    db: Session = Depends(get_db)
):
    return crud_libro.get_libri(
        db, skip=skip, limit=limit,
        didattici=didattici, senza_riservati=senza_riservati, titolo=titolo
    )

@router.get("/{libro_id}", response_model=LibroResponse)
def get_libro(libro_id: int, db: Session = Depends(get_db)):
    obj = crud_libro.get_libro(db, libro_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Libro con ID {libro_id} non trovato")
    return obj

@router.post("/", response_model=LibroResponse, status_code=201)
def create_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    return crud_libro.create_libro(db, libro)