from sqlalchemy.orm import Session
from models.ingrediente import Ingrediente
from schemas.ingrediente import IngredienteCreate, IngredienteUpdate


def get_ingredienti(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ingrediente).offset(skip).limit(limit).all()

def get_ingrediente(db: Session, ingrediente_id: int):
    return db.query(Ingrediente).filter(Ingrediente.ingrediente_id == ingrediente_id).first()

def create_ingrediente(db: Session, ingrediente: IngredienteCreate):
    # 1 Convertiamo l'ingrediente nel formato richiesto dal DB
    db_ingrediente = Ingrediente(**ingrediente.model_dump())
    """
    **model_dump crea un dizionario con chiave valore
    {"nome": "mozzarella",
    {"allergene": True,
    {"vegetariano": True,
    {"prezzo_extra": 0.0
    """
    # 2 Aggiungiamo l'ingrediente ottenuto al DB
    db.add(db_ingrediente)

    # 3 Attualizziamo in memoria (statica) la modifica
    db.commit()

    # 4 Refresh della versione in RAM -> per ottenere roba scelta dal DBMS come l'ID
    db.refresh(db_ingrediente)

    return db_ingrediente

def update_ingrediente(db: Session,ingrediente_id: int, ingrediente: IngredienteUpdate):
    # Cerchiamo l'ingrediente da modificare
    db_ingrediente = get_ingrediente(db, ingrediente_id)
    if not db_ingrediente:
        return None

    # per ogni chiave e valore del dizionario ottenuto dall'oggetto ingrediente passato
    for key, value in ingrediente.model_dump(exclude_unset=True):
        # Settiamo nell'ingrediente del DB il valore corrispondente all'attributo
        setattr(db_ingrediente, key, value)
        # non fa apparire la coppia chiave valore None: None

    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente

def delete_ingrediente(db: Session, ingrediente_id: int):
    db_ingrediente = get_ingrediente(db, ingrediente_id)
    if not db_ingrediente:
        return None

    db.delete(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente
