from sqlalchemy.orm import Session
from models.lettore import Lettore
from schemas.lettore import LettoreCreate, LettoreUpdate

def get_lettore(db: Session, lettore_id: int):
    return db.query(Lettore).filter(Lettore.lettore_id == lettore_id).first()

def get_lettori(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lettore).offset(skip).limit(limit).all()

def create_lettore(db: Session, lettore: LettoreCreate):
    db_lettore = Lettore(**lettore.model_dump())
    db.add(db_lettore)
    db.commit()
    db.refresh(db_lettore)
    return db_lettore

def update_lettore(db: Session, lettore_id: int, lettore: LettoreUpdate):
    db_lettore = get_lettore(db, lettore_id)
    if not db_lettore:
        return None
    for campo, valore in lettore.model_dump(exclude_none=True).items():
        setattr(db_lettore, campo, valore)
    db.commit()
    db.refresh(db_lettore)
    return db_lettore