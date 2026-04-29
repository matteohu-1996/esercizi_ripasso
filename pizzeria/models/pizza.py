from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from pizzeria.database import Base

class Pizza(Base):
    __tablename__ = 'pizze'
    pizza_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), unique=True, index=True)
    prezzo = Column(Float)

    # relazione: una pizza può essere richiesta in molti ordini
    ordini = relationship("Ordine", back_populates="pizza")
