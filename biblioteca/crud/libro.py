from sqlalchemy.orm import Session
from typing import List, Optional
from models.libro import Libro
from models.tag import Tag
from schemas.libro import LibroCreate, LibroUpdate

def get_libri(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        didattici: Optional[bool] = None,
        senza_riservati: Optional[bool] = None,
        titolo: Optional[str] = None,
):
    query = db.query(Libro)
    if titolo:
        query = query.filter(Libro.titolo.ilike(f"%{titolo}%"))
    libri = query.all()
    if didattici:
        libri = [l for l in libri if l.tags and all(l.didaticci for i in l.tags)]
    if senza_riservati:
        libri = [l for l in libri if not any(i.didattici for i in l.tags)]
    return libri[skip:skip + limit]

def get_libro(db: Session, libro_id: int):
    return db.query(Libro).filter(Libro.id == libro_id).first()

def create_libro(db: Session, libro: LibroCreate):
    data = libro.model_dump(exclude={"tags_ids"})
    db_libro = Libro(**data)
    if libro.tags_id:
        tags = db.query(Tag).filter(Tag.tag_id.in_(libro.tags_id)).all()
        db_libro.tags = tags
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro