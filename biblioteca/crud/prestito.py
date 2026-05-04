from sqlalchemy.orm import Session
from datetime import datetime, date, time
from models.prestito import Prestito,VocePrestito,StatoPrestito
from models.tag import Tag
from schemas.prestito import PrestitoCreate, PrestitoStatoUpdate

def create_prestito(db: Session, prestito: PrestitoCreate):
    db_prestito = Prestito(
        lettore_id=prestito.lettore_id,
        note=prestito.note,
        data_ora=datetime.now(),
        stato=StatoPrestito.PRENOTATO,
    )
    db.add(db_prestito)
    db.flush()

    for voce_data in prestito.voci:
        db_voce = VocePrestito(
            prestito_id=db_prestito.prestito_id,
            libro_id=voce_data.libro_id,
            quantita=voce_data.quantita,
        )
        if voce_data.tags_extra_ids:
            tags_extra = db.query(Tag).filter(
                Tag.prestito_id.in_(voce_data.tags_extra_ids)
            ).all()
            db_voce.tags_extra = tags_extra
        db.add(db_voce)

    db.commit()
    db.refresh(db_prestito)
    return db_prestito

def get_prestito(db: Session, prestito_id: int):
    return db.query(Prestito).filter(Prestito.prestito_id==prestito_id).first()

def aggiorna_stato(db: Session, prestito_id: int, stato_update: PrestitoStatoUpdate):
    db_prestito = get_prestito(db, prestito_id)
    if not db_prestito:
        return None
    db_prestito.stato = stato_update.stato
    db.commit()
    db.refresh(db_prestito)
    return db_prestito

def get_prestiti_oggi(db: Session):
    inizio = datetime.combine(date.today(), time.min)
    fine = datetime.combine(date.today(), time.max)
    return (
        db.query(Prestito).filter(Prestito.data_ora >= inizio, Prestito.data_ora <= fine).all().order_by(
            Prestito.data_ora.asc())
    )

def get_storico_lettore(db: Session, lettore_id: int):
    prestiti = db.query(Prestito).filter(Prestito.lettore_id==lettore_id).all()
    totale = 0.0
    for prestito in prestiti:
        for voce in prestito.voci:
            durata_base = voce.libro.durata_base + sum(i.giorni_extra for i in voce.libro.durata)
            giorni_extra = sum(i.giorni_extra for i in voce.tags_extra)
            totale += (giorni_extra + durata_base) * voce.quantita
    return prestiti, totale
