from database import SessionLocal, engine, Base
from models.lettore import Lettore
from models.libro import Libro
from models.tag import Tag
from models.prestito import Prestito, VocePrestito, StatoPrestito
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── TAG ──────────────────────────────────────────────────────────────────────
tags_data = [
    {"nome": "Classico",        "giorni_extra": 7,  "riservato": False, "didattico": True},
    {"nome": "Narrativa",       "giorni_extra": 0,  "riservato": False, "didattico": False},
    {"nome": "Poesia",          "giorni_extra": 5,  "riservato": False, "didattico": True},
    {"nome": "Teatro",          "giorni_extra": 5,  "riservato": False, "didattico": True},
    {"nome": "Filosofia",       "giorni_extra": 10, "riservato": False, "didattico": True},
    {"nome": "Storico",         "giorni_extra": 3,  "riservato": False, "didattico": False},
    {"nome": "Riservato 18+",   "giorni_extra": 0,  "riservato": True,  "didattico": False},
    {"nome": "Raro",            "giorni_extra": 0,  "riservato": True,  "didattico": False},
    {"nome": "Avventura",       "giorni_extra": 0,  "riservato": False, "didattico": False},
    {"nome": "Romantico",       "giorni_extra": 0,  "riservato": False, "didattico": False},
    {"nome": "Distopico",       "giorni_extra": 3,  "riservato": False, "didattico": True},
    {"nome": "Russo",           "giorni_extra": 7,  "riservato": False, "didattico": False},
    {"nome": "Inglese",         "giorni_extra": 0,  "riservato": False, "didattico": False},
    {"nome": "Italiano",        "giorni_extra": 0,  "riservato": False, "didattico": True},
    {"nome": "Francese",        "giorni_extra": 3,  "riservato": False, "didattico": False},
]

tags = [Tag(**t) for t in tags_data]
db.add_all(tags)
db.flush()

# indice per nome per comodità
tag = {t.nome: t for t in tags}

# ── LIBRI ─────────────────────────────────────────────────────────────────────
libri_data = [
    {
        "titolo": "I Promessi Sposi",
        "isbn": "978-88-04-40213-1",
        "anno": 1840,
        "descrizione": "Capolavoro del romanzo storico italiano di Alessandro Manzoni.",
        "durata_base": 30,
        "disponibile": True,
        "tags": [tag["Classico"], tag["Storico"], tag["Italiano"]],
    },
    {
        "titolo": "Divina Commedia",
        "isbn": "978-88-04-67950-2",
        "anno": 1320,
        "descrizione": "Il poema epico di Dante Alighieri, viaggio nell'oltretomba.",
        "durata_base": 30,
        "disponibile": True,
        "tags": [tag["Classico"], tag["Poesia"], tag["Italiano"]],
    },
    {
        "titolo": "Delitto e Castigo",
        "isbn": "978-88-06-21345-3",
        "anno": 1866,
        "descrizione": "Romanzo psicologico di Fëdor Dostoevskij.",
        "durata_base": 21,
        "disponibile": True,
        "tags": [tag["Classico"], tag["Narrativa"], tag["Russo"]],
    },
    {
        "titolo": "Anna Karenina",
        "isbn": "978-88-06-21346-4",
        "anno": 1878,
        "descrizione": "Romanzo di Lev Tolstoj sulla società russa dell'Ottocento.",
        "durata_base": 21,
        "disponibile": True,
        "tags": [tag["Classico"], tag["Romantico"], tag["Russo"]],
    },
    {
        "titolo": "1984",
        "isbn": "978-88-06-21347-5",
        "anno": 1949,
        "descrizione": "Romanzo distopico di George Orwell sul totalitarismo.",
        "durata_base": 14,
        "disponibile": True,
        "tags": [tag["Distopico"], tag["Narrativa"], tag["Inglese"]],
    },
    {
        "titolo": "Amleto",
        "isbn": "978-88-06-21348-6",
        "anno": 1603,
        "descrizione": "Tragedia di William Shakespeare.",
        "durata_base": 14,
        "disponibile": True,
        "tags": [tag["Classico"], tag["Teatro"], tag["Inglese"]],
    },
    {
        "titolo": "Il Conte di Montecristo",
        "isbn": "978-88-06-21349-7",
        "anno": 1844,
        "descrizione": "Romanzo d'avventura di Alexandre Dumas.",
        "durata_base": 21,
        "disponibile": True,
        "tags": [tag["Avventura"], tag["Storico"], tag["Francese"]],
    },
    {
        "titolo": "La Repubblica",
        "isbn": "978-88-06-21350-8",
        "anno": -380,
        "descrizione": "Dialogo filosofico di Platone sulla giustizia e lo stato ideale.",
        "durata_base": 21,
        "disponibile": True,
        "tags": [tag["Filosofia"], tag["Classico"], tag["Raro"]],
    },
]

libri = []
for data in libri_data:
    t = data.pop("tags")
    l = Libro(**data)
    l.tags = t
    db.add(l)
    libri.append(l)
db.flush()

# ── LETTORI ───────────────────────────────────────────────────────────────────
lettori_data = [
    {"nome": "Marco Rossi",    "email": "marco.rossi@email.it",    "telefono": "3331234567", "tessera": "TES-001"},
    {"nome": "Laura Bianchi",  "email": "laura.bianchi@email.it",  "telefono": "3349876543", "tessera": "TES-002"},
    {"nome": "Giovanni Verdi", "email": "giovanni.verdi@email.it", "telefono": "3356543210", "tessera": "TES-003"},
]

lettori = [Lettore(**l) for l in lettori_data]
db.add_all(lettori)
db.flush()

marco, laura, giovanni = lettori

# ── PRESTITI ──────────────────────────────────────────────────────────────────
def make_prestito(lettore, stato, giorni_fa, voci):
    p = Prestito(
        lettore_id=lettore.lettore_id,
        data_ora=datetime.now() - timedelta(days=giorni_fa),
        stato=stato,
        note=None,
    )
    db.add(p)
    db.flush()
    for libro, quantita, tags_extra in voci:
        v = VocePrestito(
            prestito_id=p.prestito_id,
            libro_id=libro.libro_id,
            quantita=quantita,
        )
        v.tags_extra = tags_extra
        db.add(v)
    return p

make_prestito(marco, StatoPrestito.RESTITUITO, 20, [
    (libri[0], 1, [tag["Classico"]]),   # I Promessi Sposi
    (libri[1], 1, []),                  # Divina Commedia
])

make_prestito(laura, StatoPrestito.RITIRATO, 5, [
    (libri[4], 1, [tag["Distopico"]]),  # 1984
])

make_prestito(giovanni, StatoPrestito.PRENOTATO, 1, [
    (libri[2], 1, []),                  # Delitto e Castigo
    (libri[6], 1, [tag["Avventura"]]),  # Il Conte di Montecristo
])

make_prestito(marco, StatoPrestito.IN_RITARDO, 15, [
    (libri[7], 1, [tag["Raro"]]),       # La Repubblica
])

make_prestito(laura, StatoPrestito.PRENOTATO, 0, [
    (libri[3], 1, [tag["Romantico"]]),  # Anna Karenina
    (libri[5], 1, []),                  # Amleto
])

db.commit()
print("✅ Database popolato con successo!")
print(f"   • {len(tags)} tag")
print(f"   • {len(libri)} libri")
print(f"   • {len(lettori)} lettori")
print(f"   • 5 prestiti")
db.close()
