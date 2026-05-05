# Cheatsheet FastAPI + SQLAlchemy + Pydantic

Riferimento rapido per esercizi tipo pizzeria / micro-blog / fatture / università.

---

## 0. Setup

```bash
pip install fastapi sqlalchemy pymysql "uvicorn[standard]" python-dotenv
uvicorn main:app --reload
```

Docs auto: `http://localhost:8000/docs` (Swagger), `/redoc`.

---

## 1. Stringa di connessione DB (LA cosa più dimenticata)

Formato:

```
linguaggio+driver://utente:password@host:porta/nome_db
```

MySQL con pymysql:

```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/nome_db"
```

- utente di default MySQL XAMPP: `root`
- password vuota: lascia stringa vuota fra `:` e `@`
- porta MySQL standard: `3306`
- DB **deve esistere già** (creare via phpMyAdmin / `CREATE DATABASE nome_db;`)

SQLite (per test rapidi, nessun server):

```python
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

PostgreSQL:

```python
DATABASE_URL = "postgresql+psycopg2://user:pwd@localhost:5432/nome_db"
```

### Versione con .env

`.env`:
```
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nome_db
```

`database.py`:
```python
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
```

---

## 2. `database.py` boilerplate

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/nome_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

---

## 3. `models.py` — SQLAlchemy ORM

### Tipi colonna comuni

| Python | SQLAlchemy        | Note                         |
|--------|-------------------|------------------------------|
| int    | `Integer`         | per id e numeri interi       |
| str    | `String(N)`       | **MySQL pretende lunghezza** |
| float  | `Float`           |                              |
| bool   | `Boolean`         |                              |
| date   | `Date`            | da `datetime.date`           |
| datetime | `DateTime`      | da `datetime.datetime`       |
| enum   | `Enum(MioEnum)`   | classe `enum.Enum`           |

### Modello base

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Pizza(Base):
    __tablename__ = "pizzas"

    pizza_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, index=True)
    price = Column(Float)

    orders = relationship("Order", back_populates="pizza")
```

Attributi `Column` utili:
- `primary_key=True` — chiave primaria
- `index=True` — crea indice (velocizza filter)
- `unique=True` — vincolo unicità
- `nullable=False` — NOT NULL
- `default=valore` — default Python
- `ForeignKey("tabella.colonna")` — chiave esterna

### Relazione 1:N

```python
# parent (User)
posts = relationship("Post", back_populates="owner")

# child (Post)
user_id = Column(Integer, ForeignKey("users.user_id"))
owner = relationship("User", back_populates="posts")
```

`back_populates` mantiene **bidirezionale**: i due lati restano sincronizzati.

### Relazione N:N (con tabella bridge)

```python
from sqlalchemy import Table

# definirla PRIMA dei modelli che la usano
pizza_ingredients = Table(
    "pizza_ingredients",
    Base.metadata,
    Column("pizza_id", Integer, ForeignKey("pizzas.pizza_id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True),
)

class Pizza(Base):
    ...
    ingredients = relationship("Ingredient", secondary=pizza_ingredients, back_populates="pizzas")

class Ingredient(Base):
    ...
    pizzas = relationship("Pizza", secondary=pizza_ingredients, back_populates="ingredients")
```

### Enum

```python
import enum
class OrderStatus(str, enum.Enum):
    RICEVUTO = "ricevuto"
    PRONTO = "pronto"

# nel modello
status = Column(Enum(OrderStatus), default=OrderStatus.RICEVUTO)
```

### Property calcolata (esposta da Pydantic)

```python
class Order(Base):
    ...
    @property
    def total(self):
        return sum(item.price * item.qty for item in self.items)
```

Lato Pydantic: dichiarala come campo normale + `from_attributes = True`.

### Cascade (eliminare i figli con il padre)

```python
items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
```

---

## 4. `schemas.py` — Pydantic

### Pattern Base / Create / Response

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class PizzaBase(BaseModel):
    name: str
    price: float

class PizzaCreate(PizzaBase):     # input POST
    pass

class Pizza(PizzaBase):           # output (response_model)
    pizza_id: int
    orders: List["Order"] = []

    class Config:
        from_attributes = True    # legge dagli oggetti SQLAlchemy
```

### Validazioni Field

```python
name: str = Field(min_length=1, max_length=80)
price: float = Field(gt=0)           # > 0
quantity: int = Field(ge=1)          # >= 1
discount: float = Field(ge=0, le=1)  # in [0, 1]
```

### Tipi utili

- `Optional[X]` o `X | None` — campo opzionale
- `List[X]` — lista
- `datetime.date` / `datetime.datetime` — passa da JSON come ISO string
- Enum dei modelli → mettilo direttamente come tipo del campo

### Ordine schemi (gotcha)

Definisci prima gli schemi **senza dipendenze**, poi quelli che li usano. Es: `Comment` prima di `Post`, `Order` prima di `Customer` (se Customer espone `orders: List[Order]`).

---

## 5. `crud.py` — operazioni DB

### Create

```python
def create_pizza(db: Session, pizza: schemas.PizzaCreate):
    db_pizza = models.Pizza(**pizza.model_dump())   # spacchetta dict in kwargs
    db.add(db_pizza)         # in RAM
    db.commit()              # scrive su disco
    db.refresh(db_pizza)     # ricarica per avere id generato
    return db_pizza
```

### Read

```python
db.query(models.Pizza).all()                                    # tutte
db.query(models.Pizza).filter(models.Pizza.pizza_id == 1).first()  # una sola
db.query(models.Pizza).offset(skip).limit(limit).all()          # paginazione
db.query(models.Pizza).count()                                  # conteggio
```

### Filter — operatori

```python
.filter(Model.col == val)           # uguale
.filter(Model.col != val)           # diverso
.filter(Model.col > val)            # >
.filter(Model.col.in_([1, 2, 3]))   # IN
.filter(Model.col.like("%abc%"))    # LIKE (case-sensitive)
.filter(Model.col.ilike("%abc%"))   # ILIKE (case-insensitive)
.filter(Model.col.is_(None))        # IS NULL
```

Concatenare = AND. Per OR:

```python
from sqlalchemy import or_, and_
.filter(or_(Model.a == 1, Model.b == 2))
```

### Order by

```python
.order_by(Model.col.asc())
.order_by(Model.col.desc())
```

### Join (passa per le ForeignKey/relationship)

```python
db.query(models.Comment)\
  .join(models.Post)\
  .join(models.User)\
  .filter(models.User.user_id == 5)\
  .all()
```

### Update

```python
obj = db.query(Model).filter(...).first()
obj.campo = nuovo_valore
db.commit()
db.refresh(obj)
```

### Delete

```python
obj = db.query(Model).filter(...).first()
db.delete(obj)
db.commit()
```

### Aggregazioni

```python
from sqlalchemy import func
db.query(func.count(Model.id)).scalar()
db.query(func.sum(Model.price)).scalar()
db.query(Model.cat, func.count()).group_by(Model.cat).all()
```

---

## 6. `main.py` — FastAPI

### Skeleton

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)   # crea le tabelle

app = FastAPI(title="...", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Endpoint

```python
@app.post("/pizzas/new", response_model=schemas.Pizza)
def create_pizza(pizza: schemas.PizzaCreate, db: Session = Depends(get_db)):
    return crud.create_pizza(db, pizza=pizza)

@app.get("/pizzas/{pizza_id}", response_model=schemas.Pizza)
def read_pizza(pizza_id: int, db: Session = Depends(get_db)):
    obj = crud.get_pizza(db, pizza_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Pizza non trovata")
    return obj

@app.get("/pizzas/", response_model=List[schemas.Pizza])
def list_pizzas(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Cerca per nome"),
    db: Session = Depends(get_db),
):
    return crud.get_pizzas(db, skip, limit, search)
```

### Tipi parametri

| Dove           | Come si dichiara             | Esempio URL              |
|----------------|------------------------------|--------------------------|
| Path param     | `/items/{id}` + arg `id: int`| `/items/3`               |
| Query param    | arg con default `q: str = ""` | `/items?q=abc`           |
| Body JSON      | arg di tipo Pydantic         | POST con corpo JSON      |
| Header         | `x: str = Header(...)`       |                          |

### Status code custom

```python
@app.post("/...", status_code=201, response_model=...)
```

### Errori

```python
raise HTTPException(status_code=404, detail="Non trovato")
```

---

## 7. Routers (per progetti più grandi tipo `fatture`)

```python
# routers/pizzas.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/pizzas", tags=["pizzas"])

@router.get("/")
def list_pizzas(...): ...

# main.py
from routers import pizzas
app.include_router(pizzas.router)
```

---

## 8. Init / seed DB

```python
# init_db.py
from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    if db.query(models.Pizza).first():
        print("già popolato")
    else:
        margherita = models.Pizza(name="Margherita", price=6.0)
        db.add(margherita)
        db.commit()
finally:
    db.close()
```

Lanciare con `python init_db.py`.

---

## 9. Errori frequenti & gotcha

| Sintomo | Causa | Fix |
|---------|-------|-----|
| `Can't connect to MySQL server` | server giù o porta sbagliata | avviare MySQL (XAMPP), porta 3306 |
| `Unknown database 'xxx'` | DB non creato | creare il DB lato server prima |
| `String type requires length on MySQL` | `String` senza N | usa `String(100)` |
| `Could not determine join condition` | manca `ForeignKey` | aggiungi `ForeignKey("tab.col")` |
| Schema risponde con id `None` | manca `db.refresh(obj)` dopo commit | aggiungi refresh |
| Pydantic ignora oggetto SQLAlchemy | manca `Config.from_attributes` | aggiungilo nello schema response |
| Import circolare schemas | dipendenze in ordine sbagliato | definisci prima il "figlio" |
| `relationship` vuota dopo create | non hai assegnato la lista o usato `back_populates` storto | assegna `parent.children = [...]` |
| `400 Bad Request` su POST | body JSON non matcha lo schema | controlla nomi campo, tipi |
| Tabelle non create | manca `Base.metadata.create_all(bind=engine)` o non importi i modelli | importa i modelli prima del create_all |
| Modello non visto da Alembic / create_all | file non importato in main.py | `import models.<file>` o `from models.x import Y` |

---

## 10. Pattern Python utili

### `**dict` unpacking

```python
data = {"name": "Margherita", "price": 6.0}
Pizza(**data)              # equivale a Pizza(name="Margherita", price=6.0)
schema.model_dump()        # Pydantic -> dict
```

### List comprehension con filtro

```python
veg = [p for p in pizzas if p.is_vegetarian]
```

### `any` / `all`

```python
all(i.is_vegetarian for i in pizza.ingredients)   # tutti vegetariani
any(i.is_allergen for i in pizza.ingredients)     # almeno un allergene
```

### `sum` con generatore

```python
total = sum(item.price * item.qty for item in items)
```

### Date di oggi

```python
from datetime import date, datetime, time, timedelta
date.today()
datetime.now()
datetime.combine(date.today(), time.min)   # inizio giornata
datetime.combine(date.today(), time.max)   # fine giornata
date.today() - timedelta(days=7)
```

---

## 11. Test rapido degli endpoint

Da `/docs` (Swagger): clicca, "Try it out", compila, esegui.

Con curl:

```bash
curl -X POST http://localhost:8000/pizzas/new \
  -H "Content-Type: application/json" \
  -d '{"name":"Margherita","price":6.0}'

curl http://localhost:8000/pizzas/1
```

Con Python `requests`:

```python
import requests
r = requests.post("http://localhost:8000/pizzas/new",
                  json={"name": "Margherita", "price": 6.0})
print(r.json())
```

---

## 12. Checklist mentale prima di consegnare

- [ ] DB esistente sul server, URL giusto in `database.py`
- [ ] Tutti i `String` hanno una lunghezza
- [ ] Ogni FK ha la sua `relationship` con `back_populates`
- [ ] Ogni schema response ha `from_attributes = True`
- [ ] `Base.metadata.create_all(bind=engine)` chiamato in `main.py`
- [ ] Modelli importati prima di `create_all` (altrimenti tabelle non create)
- [ ] `db.commit()` e `db.refresh()` dopo ogni create
- [ ] `HTTPException(404)` quando l'oggetto non esiste
- [ ] Endpoint hanno `response_model`
- [ ] Tutti i tipi negli schemi sono coerenti con i Column
- [ ] Server avviato: `uvicorn main:app --reload`
