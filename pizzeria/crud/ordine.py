from sqlalchemy.orm import Session
from datetime import date, datetime, time
from models.ordine import Ordine, VocePizzaOrdine, StatoOrdine
from models.ingrediente import Ingrediente
from schemas.ordine import OrdineCreate, OrdineStatoUpdate


def create_ordine(db: Session, ordine: OrdineCreate):
    db_ordine = Ordine(
        cliente_id=ordine.cliente_id,
        note=ordine.note,
        data_ora=datetime.now(),
        stato=StatoOrdine.RICEVUTO,
    )
    db.add(db_ordine)
    db.flush()

    for voce_data in ordine.voci:
        db_voce = VocePizzaOrdine(
            ordine_id=db_ordine.ordine_id,
            pizza_id=voce_data.pizza_id,
            quantita=voce_data.quantita,
        )
        if voce_data.ingredienti_extra_ids:
            ingredienti_extra = db.query(Ingrediente).filter(
                Ingrediente.ingrediente_id.in_(voce_data.ingredienti_extra_ids)
            ).all()
            db_voce.ingredienti_extra = ingredienti_extra
        db.add(db_voce)

    db.commit()
    db.refresh(db_ordine)
    return db_ordine


def get_ordine(db: Session, ordine_id: int):
    return db.query(Ordine).filter(Ordine.ordine_id == ordine_id).first()


def aggiorna_stato(db: Session, ordine_id: int, stato_update: OrdineStatoUpdate):
    db_ordine = get_ordine(db, ordine_id)
    if not db_ordine:
        return None
    db_ordine.stato = stato_update.stato
    db.commit()
    db.refresh(db_ordine)
    return db_ordine


def get_ordini_oggi(db: Session):
    inizio = datetime.combine(date.today(), time.min)
    fine = datetime.combine(date.today(), time.max)
    return (
        db.query(Ordine)
        .filter(Ordine.data_ora >= inizio, Ordine.data_ora <= fine)
        .order_by(Ordine.data_ora.asc())
        .all()
    )


def get_storico_cliente(db: Session, cliente_id: int):
    ordini = db.query(Ordine).filter(Ordine.cliente_id == cliente_id).all()
    totale = 0.0
    for ordine in ordini:
        for voce in ordine.voci:
            prezzo_pizza = voce.pizza.prezzo_base + sum(i.prezzo_extra for i in voce.pizza.ingredienti)
            prezzo_extra = sum(i.prezzo_extra for i in voce.ingredienti_extra)
            totale += (prezzo_pizza + prezzo_extra) * voce.quantita
    return ordini, totale
