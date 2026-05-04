from sqlalchemy.orm import Session
from typing import Optional
from models.pizza import Pizza
from models.ingrediente import Ingrediente
from schemas.pizza import PizzaCreate, PizzaUpdate


def get_pizze(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vegetariane: Optional[bool] = None,
    senza_allergeni: Optional[bool] = None,
    nome: Optional[str] = None,
):
    query = db.query(Pizza)
    if nome:
        query = query.filter(Pizza.nome.ilike(f"%{nome}%"))
    pizze = query.all()
    if vegetariane:
        pizze = [p for p in pizze if p.ingredienti and all(i.vegetariano for i in p.ingredienti)]
    if senza_allergeni:
        pizze = [p for p in pizze if not any(i.allergene for i in p.ingredienti)]
    return pizze[skip : skip + limit]


def get_pizza(db: Session, pizza_id: int):
    return db.query(Pizza).filter(Pizza.pizza_id == pizza_id).first()


def create_pizza(db: Session, pizza: PizzaCreate):
    data = pizza.model_dump(exclude={"ingredienti_ids"})
    db_pizza = Pizza(**data)
    if pizza.ingredienti_ids:
        ingredienti = db.query(Ingrediente).filter(
            Ingrediente.ingrediente_id.in_(pizza.ingredienti_ids)
        ).all()
        db_pizza.ingredienti = ingredienti
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza


def update_pizza(db: Session, pizza_id: int, pizza: PizzaUpdate):
    db_pizza = get_pizza(db, pizza_id)
    if not db_pizza:
        return None
    data = pizza.model_dump(exclude_unset=True, exclude={"ingredienti_ids"})
    for key, value in data.items():
        setattr(db_pizza, key, value)
    if pizza.ingredienti_ids is not None:
        ingredienti = db.query(Ingrediente).filter(
            Ingrediente.ingrediente_id.in_(pizza.ingredienti_ids)
        ).all()
        db_pizza.ingredienti = ingredienti
    db.commit()
    db.refresh(db_pizza)
    return db_pizza


def delete_pizza(db: Session, pizza_id: int):
    db_pizza = get_pizza(db, pizza_id)
    if not db_pizza:
        return None
    db_pizza.disponibile = False
    db.commit()
    db.refresh(db_pizza)
    return db_pizza
